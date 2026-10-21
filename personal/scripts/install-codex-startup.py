#!/usr/bin/env python3
"""Synchronize the canonical skill body into a managed Codex startup block."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import tempfile

BEGIN = "<!-- ponytail-pragmatic:begin -->"
END = "<!-- ponytail-pragmatic:end -->"


def render(skill_bytes, skill_path, template):
    text = skill_bytes.decode("utf-8")
    frontmatter = re.match(r"\A---\r?\n.*?\r?\n---\r?\n", text, re.DOTALL)
    if frontmatter is None:
        raise ValueError("The canonical skill must have YAML frontmatter.")
    body = text[frontmatter.end():].strip()
    if not body:
        raise ValueError("The canonical skill body is empty.")
    values = {
        "{{SKILL_PATH}}": str(skill_path),
        "{{SKILL_SHA256}}": hashlib.sha256(skill_bytes).hexdigest(),
        "{{SKILL_BODY}}": body,
    }
    for key, value in values.items():
        if template.count(key) != 1:
            raise ValueError("The startup template must contain exactly one " + key)
        template = template.replace(key, value)
    return template.strip()


def merge(existing, block):
    starts, ends = existing.count(BEGIN), existing.count(END)
    if starts == ends == 0:
        separator = "" if not existing or existing.endswith("\n\n") else "\n" if existing.endswith("\n") else "\n\n"
        return existing + separator + block + "\n"
    if starts != 1 or ends != 1:
        raise ValueError("Duplicate or incomplete managed startup markers; no file was changed.")
    start, end = existing.index(BEGIN), existing.index(END)
    if end < start:
        raise ValueError("Managed startup markers are out of order; no file was changed.")
    return existing[:start] + block + existing[end + len(END):]


def synchronize(codex_home, personal_root, check=False):
    source = personal_root / "skills/ponytail-pragmatic/SKILL.md"
    installed = codex_home / "skills/ponytail-pragmatic/SKILL.md"
    if not installed.is_file() or installed.read_bytes() != source.read_bytes():
        raise ValueError("Install this exact skill revision before synchronizing startup guidance.")
    override = codex_home / "AGENTS.override.md"
    if override.is_file() and override.read_text(encoding="utf-8").strip():
        raise ValueError("A nonempty global AGENTS.override.md is active; resolve its precedence first.")
    target = codex_home / "AGENTS.md"
    if target.is_symlink():
        raise ValueError("The global AGENTS.md is a symlink; resolve its intended target first.")
    existing = ""
    if target.exists():
        with target.open(encoding="utf-8", newline="") as handle:
            existing = handle.read()
    template = (personal_root / "codex-global-guidance.md").read_text(encoding="utf-8")
    updated = merge(existing, render(source.read_bytes(), installed, template))
    if check:
        if existing != updated:
            raise ValueError("Startup guidance is missing or stale.")
        return "Startup guidance matches the installed skill."
    if existing == updated:
        return "Startup guidance is already current."
    if target.exists():
        backup_dir = codex_home / "backups/ponytail-pragmatic"
        backup_dir.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        backup = backup_dir / ("AGENTS-" + digest + ".md")
        if not backup.exists():
            shutil.copy2(target, backup)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=codex_home, prefix=".ponytail-startup-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(updated.encode("utf-8"))
        temporary.chmod(target.stat().st_mode & 0o777 if target.exists() else 0o644)
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return "Updated the managed startup block; unrelated global guidance was preserved."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser())
    parser.add_argument("--check", action="store_true", help="Check synchronization without writing files.")
    args = parser.parse_args()
    try:
        print(synchronize(args.codex_home, Path(__file__).resolve().parents[1], args.check))
    except (OSError, ValueError) as error:
        parser.exit(1, "Error: " + str(error) + "\n")


if __name__ == "__main__":
    main()
