"""Check project documents and run the configured checks without a shell."""

import argparse
import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote

import yaml

SKIP = {".git", ".venv", "node_modules", ".artifacts", "__pycache__", "target", "dist", "build"}


def tracked_candidates(root: Path):
    for directory, names, files in os.walk(root):
        names[:] = [name for name in names if name not in SKIP and not (Path(directory) / name).is_symlink()]
        for name in files:
            path = Path(directory) / name
            if not path.is_symlink() and ".specify/workflows/runs/" not in path.relative_to(root).as_posix():
                yield path


def headings(text: str) -> set[str]:
    result = set()
    counts: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def validate(root: Path) -> list[str]:
    errors = []
    for path in tracked_candidates(root):
        relative = path.relative_to(root)
        if "raw-materials" in relative.parts or ".specify/templates/" in relative.as_posix():
            continue
        if relative.parts[0] == "templates" and (path.name != "README.md" or "files" in relative.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        try:
            if path.suffix in {".yaml", ".yml"}:
                yaml.safe_load(text)
            elif path.suffix == ".json":
                json.loads(text)
            elif path.suffix == ".py":
                ast.parse(text, filename=str(relative))
            elif path.suffix == ".md":
                prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", prose):
                    if re.match(r"^[a-zA-Z][\w+.-]*:", target):
                        continue
                    name, _, fragment = unquote(target).partition("#")
                    dest = (path.parent / name).resolve() if name else path
                    if not dest.exists():
                        errors.append(f"{relative}: Linkziel fehlt: {target}")
                    elif fragment and dest.is_file() and dest.suffix == ".md":
                        if fragment not in headings(dest.read_text(encoding="utf-8")):
                            errors.append(f"{relative}: Anker fehlt: {target}")
        except (ValueError, SyntaxError, yaml.YAMLError) as error:
            errors.append(f"{relative}: {error}")
    for name in ("vision.md", "architecture.md", "development.md", "operations.md"):
        if (root / "docs" / name).exists():
            errors.append(f"docs/{name}: Inhalt gehört in docs/DV_KONZEPT.md")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Dokumentlinks und Dateisyntax: OK", flush=True)
    if args.static_only:
        return 0
    config = yaml.safe_load((root / "config/project.yaml").read_text(encoding="utf-8"))
    for command in config.get("checks", []):
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            raise ValueError("Jede Prüfung muss eine nicht leere Liste von Argumenten sein.")
        command = list(command)
        command[0] = sys.executable if command[0] == "python" else (shutil.which(command[0]) or command[0])
        print("Prüfung:", " ".join(command), flush=True)
        result = subprocess.run(command, cwd=root, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
