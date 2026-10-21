"""Check preservation, source synchronization, and refusal boundaries offline."""

import hashlib
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

PERSONAL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("codex_startup", PERSONAL / "scripts/install-codex-startup.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StartupGuidanceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.home = Path(self.directory.name)
        self.installed = self.home / "skills/ponytail-pragmatic"
        shutil.copytree(PERSONAL / "skills/ponytail-pragmatic", self.installed)
        self.target = self.home / "AGENTS.md"

    def test_complete_body_is_present_without_task_matching(self):
        MODULE.synchronize(self.home, PERSONAL)
        skill = (self.installed / "SKILL.md").read_bytes()
        result = self.target.read_text()
        self.assertIn(hashlib.sha256(skill).hexdigest(), result)
        self.assertIn("## Choose the smallest complete solution", result)
        self.assertIn("## Communicate clearly", result)
        self.assertNotIn("{{SKILL_BODY}}", result)
        self.assertNotIn("description: >", result)

    def test_existing_guidance_and_idempotence(self):
        before = "# Personal rules\nKeep this exact wording.\n\n"
        after = "\n\n# Other preferences\nKeep these too.\n"
        self.target.write_text(before + MODULE.BEGIN + "\nOld routing\n" + MODULE.END + after)
        MODULE.synchronize(self.home, PERSONAL)
        first = self.target.read_bytes()
        self.assertTrue(first.decode().startswith(before))
        self.assertTrue(first.decode().endswith(after))
        MODULE.synchronize(self.home, PERSONAL)
        self.assertEqual(first, self.target.read_bytes())
        MODULE.synchronize(self.home, PERSONAL, check=True)

    def test_check_is_read_only_and_detects_stale_guidance(self):
        self.target.write_text("Original content\n")
        with self.assertRaises(ValueError):
            MODULE.synchronize(self.home, PERSONAL, check=True)
        self.assertEqual("Original content\n", self.target.read_text())

    def test_existing_crlf_bytes_are_preserved(self):
        prefix = b"# Personal rules\r\nKeep these bytes.\r\n\r\n"
        suffix = b"\r\n# Other rules\r\nKeep these too.\r\n"
        self.target.write_bytes(prefix + MODULE.BEGIN.encode() + b"\nOld\n" + MODULE.END.encode() + suffix)
        MODULE.synchronize(self.home, PERSONAL)
        updated = self.target.read_bytes()
        self.assertTrue(updated.startswith(prefix))
        self.assertTrue(updated.endswith(suffix))

    def test_malformed_markers_do_not_change_the_file(self):
        for text in [MODULE.BEGIN, MODULE.END, MODULE.END + MODULE.BEGIN, MODULE.BEGIN + MODULE.BEGIN + MODULE.END]:
            with self.subTest(text=text):
                self.target.write_text(text)
                with self.assertRaises(ValueError):
                    MODULE.synchronize(self.home, PERSONAL)
                self.assertEqual(text, self.target.read_text())

    def test_active_override_is_not_silently_ignored(self):
        (self.home / "AGENTS.override.md").write_text("Active override\n")
        with self.assertRaises(ValueError):
            MODULE.synchronize(self.home, PERSONAL)
        self.assertFalse(self.target.exists())

    def test_missing_or_different_installed_revision_is_rejected(self):
        skill = self.installed / "SKILL.md"
        skill.write_text("Different revision\n")
        with self.assertRaises(ValueError):
            MODULE.synchronize(self.home, PERSONAL)
        skill.unlink()
        with self.assertRaises(ValueError):
            MODULE.synchronize(self.home, PERSONAL)
        self.assertFalse(self.target.exists())

    def test_backup_preserves_previous_contents(self):
        self.target.write_text("Existing personal instructions\n")
        old = self.target.read_bytes()
        MODULE.synchronize(self.home, PERSONAL)
        backups = list((self.home / "backups/ponytail-pragmatic").glob("*.md"))
        self.assertEqual(1, len(backups))
        self.assertEqual(old, backups[0].read_bytes())

    def test_symlink_target_is_not_followed(self):
        destination = self.home / "other-instructions.md"
        destination.write_text("Do not change this file.\n")
        self.target.symlink_to(destination)
        with self.assertRaises(ValueError):
            MODULE.synchronize(self.home, PERSONAL)
        self.assertEqual("Do not change this file.\n", destination.read_text())


if __name__ == "__main__":
    unittest.main()
