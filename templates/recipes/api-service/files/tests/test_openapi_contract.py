"""Check the committed contract against generated operations and schemas."""

import json
from pathlib import Path

from app.main import app

CONTRACT = Path(__file__).resolve().parents[1] / "openapi/openapi.json"


def test_contract_matches_implementation():
    committed = json.loads(CONTRACT.read_text(encoding="utf-8"))
    generated = app.openapi()
    assert committed["paths"] == generated["paths"]
    assert committed.get("components", {}) == generated.get("components", {})


def test_internal_references_resolve():
    document = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def walk(value):
        if isinstance(value, dict):
            ref = value.get("$ref")
            if ref:
                assert ref.startswith("#/"), f"External reference needs explicit validation: {ref}"
                target = document
                for part in ref[2:].split("/"):
                    target = target[part.replace("~1", "/").replace("~0", "~")]
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)
