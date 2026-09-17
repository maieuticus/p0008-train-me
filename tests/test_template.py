"""Exercise generated projects, overwrite protection and reference isolation."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check import validate
from container_init import prepare
from create_project import create_project, render_files


class ProjectGenerationTests(unittest.TestCase):
    def generate(self, directory, stack="none", services=None, recipe=None):
        destination = Path(directory) / "project"
        create_project(destination, render_files("test-project", stack, services or [], recipe))
        return destination

    def test_profiles_produce_consistent_self_contained_projects(self):
        for stack in ("none", "python", "typescript", "java-maven"):
            with self.subTest(stack=stack), TemporaryDirectory() as directory:
                root = self.generate(directory, stack)
                self.assertEqual(validate(root), [])
                self.assertTrue((root / "docs/DV_KONZEPT.md").is_file())
                self.assertFalse((root / "templates").exists())
                self.assertFalse((root / ".env").exists())
                self.assertFalse((root / ".specify/integration.json").exists())
                self.assertFalse(any(root.rglob("*sport_app*")))
                if stack == "java-maven":
                    self.assertTrue((root / "src/test/java/example/AppTest.java").is_file())
                    self.assertFalse((root / "tests").exists())

    def test_services_have_valid_files_and_only_read_access_to_foreign_contents(self):
        with TemporaryDirectory() as directory:
            root = self.generate(directory, "python", ["postgres", "keycloak", "observability"])
            self.assertEqual(validate(root), [])
            compose = yaml.safe_load((root / ".devcontainer/compose.yaml").read_text())
            container = json.loads((root / ".devcontainer/devcontainer.json").read_text())
            self.assertEqual(set(container["runServices"]), set(compose["services"]))
            self.assertEqual(set(compose["services"]), {"dev", "postgres", "keycloak", "grafana", "prometheus"})
            for service in compose["services"].values():
                self.assertNotIn("privileged", service)
                self.assertNotIn("ports", service)
                for volume in service.get("volumes", []):
                    if isinstance(volume, dict):
                        self.assertNotIn("docker.sock", volume["source"])
                        self.assertTrue((root / ".devcontainer" / volume["source"]).resolve().exists())
                        if volume["target"] != "/workspaces/project":
                            self.assertTrue(volume["read_only"])
            permissions = container["customizations"]["codespaces"]["repositories"]["maieuticus/*"]["permissions"]
            self.assertEqual(permissions, {"contents": "read", "issues": "write"})

    def test_api_recipe_selects_python_postgres_and_contract_tests(self):
        files = render_files("my-api", "none", [], "api-service")
        config = yaml.safe_load(files["config/project.yaml"])
        self.assertEqual(config["stack"], "python")
        self.assertEqual(config["services"], ["postgres"])
        self.assertIn("openapi/openapi.json", files)
        self.assertIn("tests/test_openapi_contract.py", files)
        self.assertIn("RUN_DATABASE_TESTS=1", files[".github/workflows/ci.yml"].decode())
        self.assertNotIn("POSTGRES_PASSWORD:", files[".github/workflows/ci.yml"].decode())

    def test_rejects_populated_destination_without_touching_it(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            sentinel = root / "user.txt"
            sentinel.write_text("preserve", encoding="utf-8")
            with self.assertRaises(ValueError):
                create_project(root, {"user.txt": b"overwrite"})
            self.assertEqual(sentinel.read_text(), "preserve")
            self.assertEqual(len(list(root.iterdir())), 1)

    def test_rejects_invalid_names_incompatible_profiles_and_path_escape(self):
        for name in ("../escape", "name/other", "--option", "name\nother"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                render_files(name, "python", [])
        with self.assertRaises(ValueError):
            render_files("test", "typescript", [], "api-service")
        with TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            with self.assertRaises(ValueError):
                create_project(root, {"../escape": b"no"})
            self.assertFalse(root.exists())

    def test_dry_run_creates_nothing(self):
        with TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = Path(directory) / "project"
            create_project(root, {"README.md": b"example"}, dry_run=True)
            self.assertFalse(root.exists())

    def test_static_checks_reject_split_concept_and_broken_links(self):
        with TemporaryDirectory() as directory:
            root = self.generate(directory)
            (root / "docs/architecture.md").write_text("# Duplicate", encoding="utf-8")
            (root / "README.md").write_text("[broken](missing.md)", encoding="utf-8")
            errors = validate(root)
            self.assertTrue(any("architecture.md" in error for error in errors))
            self.assertTrue(any("missing.md" in error for error in errors))


class ContainerTests(unittest.TestCase):
    def test_readonly_mount_random_secrets_and_preservation(self):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {"CODESPACES": "false", "REFERENCE_REPOS_ROOT": ""}):
            root = Path(directory) / "project"
            root.mkdir()
            (root / ".devcontainer").mkdir()
            (root / ".env.example").write_text("PASSWORD=__GENERATE__\nOTHER=__GENERATE__\n", encoding="utf-8")
            refs = Path(directory) / "references"
            refs.mkdir()
            prepare(root, str(refs))
            env = (root / ".env").read_bytes()
            self.assertNotIn(b"__GENERATE__", env)
            self.assertNotEqual(env.splitlines()[0].split(b"=")[1], env.splitlines()[1].split(b"=")[1])
            prepare(root)
            self.assertEqual(env, (root / ".env").read_bytes())
            override = yaml.safe_load((root / ".devcontainer/compose.local.yaml").read_text())
            mount = override["services"]["dev"]["volumes"][0]
            self.assertTrue(mount["read_only"])
            self.assertFalse(mount["bind"]["create_host_path"])
            self.assertEqual(mount["target"], "/references/repos")

    def test_missing_reference_fails_before_writing_local_configuration(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".devcontainer").mkdir()
            with patch.dict(os.environ, {"CODESPACES": "false"}), self.assertRaises(FileNotFoundError):
                prepare(root, str(root / "missing"))
            self.assertFalse((root / ".devcontainer/compose.local.yaml").exists())


if __name__ == "__main__":
    unittest.main()
