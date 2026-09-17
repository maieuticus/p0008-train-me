"""Clone a configured contribution target and create a branch; never push or publish."""

import argparse
from pathlib import Path
import re
import subprocess

import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=["template", "knowledge"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--branch", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    config = yaml.safe_load((root / "config/repositories.yaml").read_text(encoding="utf-8"))
    repo = config["contribution_targets"][args.target]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        parser.error("Ungültiger Repository-Name.")
    subprocess.run(["git", "check-ref-format", "--branch", args.branch], check=True)
    target = args.output.resolve()
    if target.exists() or str(target).startswith("/references/"):
        parser.error("Ein neues Ziel außerhalb von /references/ ist erforderlich.")
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--", f"https://github.com/{repo}.git", str(target)], check=True)
    subprocess.run(["git", "-C", str(target), "switch", "-c", args.branch], check=True)
    print(f"Beitrag vorbereiten: {target}. Zuerst README.md und AGENTS.md des Ziels lesen.")
    print("Es wurde nichts gepusht und kein Issue oder Pull Request veröffentlicht.")


if __name__ == "__main__":
    main()
