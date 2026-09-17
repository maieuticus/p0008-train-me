"""Prepare ignored host-local files before Compose starts. Standard library only."""

import argparse
import json
import os
from pathlib import Path
import secrets


def prepare(root: Path, references_root: str | None = None) -> None:
    local_path = root / ".devcontainer/local.json"
    local = json.loads(local_path.read_text(encoding="utf-8")) if local_path.exists() else {}
    reference = references_root or os.environ.get("REFERENCE_REPOS_ROOT") or local.get("references_root")
    override: dict = {"services": {"dev": {}}}
    if reference:
        if os.environ.get("CODESPACES") == "true":
            raise ValueError("Lokale Host-Mounts sind in Codespaces nicht verfügbar.")
        source = Path(reference).expanduser().resolve(strict=True)
        if not source.is_dir():
            raise ValueError("Der Referenzpfad muss ein Verzeichnis sein.")
        override["services"]["dev"]["volumes"] = [{
            "type": "bind", "source": str(source), "target": "/references/repos",
            "read_only": True, "bind": {"create_host_path": False},
        }]
        local["references_root"] = str(source)
    elif os.environ.get("CODESPACES") != "true":
        print("Keine Referenz-Repos eingebunden. Optional: REFERENCE_REPOS_ROOT setzen.")
    # JSON is valid YAML; generated local configuration is intentionally not committed.
    (root / ".devcontainer/compose.local.yaml").write_text(
        json.dumps(override, indent=2) + "\n", encoding="utf-8"
    )
    if local:
        local_path.write_text(json.dumps(local, indent=2) + "\n", encoding="utf-8")
    env_path = root / ".env"
    if not env_path.exists():
        example = (root / ".env.example").read_text(encoding="utf-8")
        lines = [
            line.replace("__GENERATE__", secrets.token_urlsafe(24)) if "__GENERATE__" in line else line
            for line in example.splitlines()
        ]
        with env_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write("\n".join(lines) + "\n")
        if os.name != "nt":
            env_path.chmod(0o600)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references-root")
    args = parser.parse_args()
    try:
        prepare(Path(__file__).resolve().parents[1], args.references_root)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
