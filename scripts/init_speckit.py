"""Initialize the pinned Spec Kit integration, preserving project-owned overrides."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integration", default="copilot")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if (root / ".specify/integration.json").exists():
        parser.error("Bereits initialisiert. Für Updates: specify integration upgrade <integration>.")
    config = yaml.safe_load((root / "config/project.yaml").read_text(encoding="utf-8"))
    version = config["speckit_version"]
    specify = shutil.which("specify")
    if specify:
        installed = subprocess.run([specify, "version"], capture_output=True, text=True, check=True)
        if str(version) not in installed.stdout:
            parser.error(f"Spec Kit {version} erforderlich. Installierte Version: {installed.stdout.strip()}")
        command = [specify]
    elif shutil.which("uvx"):
        command = ["uvx", "--from", f"specify-cli=={version}", "specify"]
    else:
        parser.error(f"Spec Kit installieren: python -m pip install specify-cli=={version}")
    constitution = root / ".specify/memory/constitution.md"
    original = constitution.read_bytes()
    try:
        result = subprocess.run(
            command + ["init", "--here", "--integration", args.integration,
                       "--script", "sh", "--force"],
            cwd=root, check=False,
        )
    finally:
        constitution.write_bytes(original)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
