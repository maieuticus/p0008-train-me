"""Create a project from selected modules; never modify a populated destination."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
STACKS = ("none", "python", "typescript", "java-maven")
SERVICES = ("postgres", "keycloak", "observability")
CORE_FILES = (
    "AGENTS.md", ".gitignore", ".gitattributes", ".editorconfig", ".dockerignore", ".env.example",
    ".devcontainer/Dockerfile", "config/repositories.yaml",
    "scripts/check.py", "scripts/container_init.py", "scripts/init_speckit.py",
    "scripts/prepare_contribution.py", "scripts/requirements.txt",
    "docs/decisions/README.md",
)
CORE_TREES = (
    ".vscode", ".github/ISSUE_TEMPLATE", ".specify/memory",
    ".specify/templates/overrides", ".specify/workflows/project-sdd",
)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_yaml(value) -> bytes:
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False).encode("utf-8")


def add_tree(files: dict[str, bytes], source: Path, prefix: str = "") -> None:
    if not source.exists():
        return
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks sind keine Template-Dateien: {path}")
        if path.is_file():
            relative = path.relative_to(source).as_posix()
            target = f"{prefix}/{relative}" if prefix else relative
            if target.endswith(".template"):
                target = target.removesuffix(".template")
            files[target] = path.read_bytes()


def render_files(name: str, stack: str, services: list[str], recipe: str | None = None):
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name):
        raise ValueError("Projektname: Kleinbuchstaben, Ziffern und einzelne Bindestriche.")
    if stack not in STACKS or any(service not in SERVICES for service in services):
        raise ValueError("Unbekanntes Technologieprofil oder unbekannter Dienst.")
    if recipe not in (None, "api-service"):
        raise ValueError("Unbekanntes Rezept.")
    if recipe:
        if stack not in ("none", "python"):
            raise ValueError("api-service benötigt das Python-Profil.")
        stack = "python"
        services = list(dict.fromkeys([*services, "postgres"]))
    services = sorted(set(services))
    files = {path: (ROOT / path).read_bytes() for path in CORE_FILES}
    for tree in CORE_TREES:
        add_tree(files, ROOT / tree, tree)
    add_tree(files, ROOT / "templates/base/files")
    files[".github/PULL_REQUEST_TEMPLATE.md"] = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_bytes()
    config = deepcopy(load_yaml(ROOT / "config/project.yaml"))
    config.update(name=name, kind="project", stack=stack, services=services, recipe=recipe, checks=[])
    try:
        ref = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
        config["template_revision"] = ref + ("+working-tree" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        config["template_revision"] = "unversioned"
    container = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text(encoding="utf-8"))
    container["name"] = name
    compose = load_yaml(ROOT / ".devcontainer/compose.yaml")
    setup = ["python -m pip install -r scripts/requirements.txt"]
    if stack != "none":
        module = ROOT / "templates/stacks" / stack
        meta = load_yaml(module / "module.yaml")
        add_tree(files, module / "files")
        container["features"].update(meta.get("features", {}))
        config["checks"] = meta["checks"]
        setup.extend(meta.get("setup", []))
    env = {}
    for service in services:
        module = ROOT / "templates/services" / service
        meta = load_yaml(module / "module.yaml")
        add_tree(files, module / "files")
        fragment = load_yaml(module / "compose.yaml")
        for section in ("services", "volumes"):
            for key, value in fragment.get(section, {}).items():
                if key in compose.setdefault(section, {}):
                    raise ValueError(f"Doppelte Compose-Komponente: {key}")
                compose[section][key] = value
        for key, value in meta.get("environment", {}).items():
            if key in env:
                raise ValueError(f"Doppelte Umgebungsvariable: {key}")
            env[key] = value
        container.setdefault("forwardPorts", []).extend(meta.get("forward_ports", []))
    if recipe:
        module = ROOT / "templates/recipes/api-service"
        meta = load_yaml(module / "module.yaml")
        add_tree(files, module / "files")
        config["checks"] = meta["checks"]
        setup = meta["setup"]
        container.setdefault("forwardPorts", []).append(8000)
        config["recipe"] = recipe
        principles = (module / "constitution/api-service-principles.md").read_text(encoding="utf-8")
        files[".specify/memory/constitution.md"] += (
            "\n\n## API-Service-Ergänzungen\n\n### " + principles.split("## ", 1)[1].replace("\n## ", "\n### ")
        ).encode("utf-8")
    # All selected services are explicitly started by Dev Containers.
    container["runServices"] = list(compose["services"])
    files[".devcontainer/devcontainer.json"] = (json.dumps(container, indent=2) + "\n").encode()
    files[".devcontainer/compose.yaml"] = dump_yaml(compose)
    files["config/project.yaml"] = dump_yaml(config)
    files[".env.example"] = (
        "# Ausschließlich lokale Entwicklung; container_init.py erzeugt fehlende Secrets.\n"
        + "".join(f"{key}={value}\n" for key, value in env.items())
    ).encode()
    substitutions = {
        "{{PROJECT_NAME}}": name, "{{STACK}}": stack,
        "{{SERVICES}}": ", ".join(services) or "keine",
        "{{RECIPE}}": recipe or "keines", "{{SETUP_COMMANDS}}": "\n".join(setup),
        "{{CHECK_COMMANDS}}": "\n".join(" ".join(c) for c in config["checks"]) or
        "# Noch kein Anwendungscode; gemeinsame Dokument- und Syntaxprüfung.",
    }
    for target, data in files.items():
        for old, new in substitutions.items():
            data = data.replace(old.encode(), new.encode())
        files[target] = data
    return files


def create_project(output: Path, files: dict[str, bytes], dry_run: bool = False) -> None:
    if output.is_symlink():
        raise ValueError("Das Ziel darf kein Symlink sein.")
    output = output.resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        raise ValueError("Das Template oder eines seiner Elternverzeichnisse ist kein Projektziel.")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Das Ziel muss fehlen oder leer sein. Bestehende Dateien werden nicht überschrieben.")
    for relative in files:
        candidate = (output / relative).resolve()
        if not candidate.is_relative_to(output):
            raise ValueError(f"Ungültiger Zielpfad: {relative}")
    if dry_run:
        print("\n".join(sorted(files)))
        return
    output.mkdir(parents=True, exist_ok=True)
    for relative, data in files.items():
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(data)
    print(f"Projekt erstellt: {output} ({len(files)} Dateien)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--stack", choices=STACKS, default="none")
    parser.add_argument("--service", choices=SERVICES, action="append", default=[])
    parser.add_argument("--recipe", choices=["api-service"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        create_project(args.output, render_files(args.name, args.stack, args.service, args.recipe), args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
