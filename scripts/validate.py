#!/usr/bin/env python3
"""Fresh-checkout checks for this repo.

1. Every .json file parses.
2. Every relative path referenced in .claude-plugin/*.json and
   .codex-plugin/*.json exists.
3. Every SKILL.md under .agents/skills and community has frontmatter with a
   name (matching its folder) and a description.
4. No symlinks anywhere.
5. With --check-mirror-state: .mirror-state.json exists and matches the hash
   of the managed paths. CI runs this on main only, so pull requests that
   touch official paths still pass; a maintainer ports them.

The managed-path hash is the SHA-256 of a manifest with one
"<mode> <sha256 hex>  <path>" line per file under the managed paths, sorted
by path in byte order, where <mode> is 100755 for an executable file and
100644 otherwise. The mirror job in Flaim's main codebase computes the same
hash, and its managed-path list must match MANAGED_PATHS below.

Usage: python3 scripts/validate.py [--check-mirror-state] [repo-root]
"""

import glob
import hashlib
import json
import os
import sys

# Mirrored from Flaim's main codebase. Hardcoded here, not read from the state
# file, so an edited state file can't shrink what the hash covers.
MANAGED_PATHS = [
    ".agents/skills",
    ".claude-plugin",
    ".codex-plugin",
    ".mcp.json",
    "server.json",
    "glama.json",
    "gemini-extension.json",
]

errors = []


def fail(message):
    errors.append(message)


def walk_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in dirnames + filenames:
            yield os.path.join(dirpath, name)


def managed_files(root, managed_paths):
    files = []
    for managed in managed_paths:
        full = os.path.join(root, managed)
        if os.path.isfile(full):
            files.append(managed)
        elif os.path.isdir(full):
            for dirpath, _, filenames in os.walk(full):
                for name in filenames:
                    files.append(os.path.relpath(os.path.join(dirpath, name), root))
    return sorted(set(files), key=lambda path: path.encode("utf-8"))


def managed_hash(root, managed_paths):
    manifest = ""
    for path in managed_files(root, managed_paths):
        full = os.path.join(root, path)
        with open(full, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
        mode = "100755" if os.access(full, os.X_OK) else "100644"
        manifest += f"{mode} {digest}  {path}\n"
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest()


def check_json(root):
    parsed = {}
    for path in walk_files(root):
        if path.endswith(".json") and os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as handle:
                    parsed[path] = json.load(handle)
            except (ValueError, OSError) as error:
                fail(f"{os.path.relpath(path, root)}: invalid JSON ({error})")
    return parsed


def referenced_paths(value):
    if isinstance(value, str):
        if value.startswith("./"):
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from referenced_paths(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from referenced_paths(item)


def check_manifest_paths(root, parsed):
    manifests = glob.glob(os.path.join(root, ".claude-plugin", "*.json")) + glob.glob(
        os.path.join(root, ".codex-plugin", "*.json")
    )
    for manifest in manifests:
        data = parsed.get(manifest)
        if data is None:
            continue
        # Plugin paths are relative to the plugin root, which is the repo root.
        for ref in referenced_paths(data):
            if not os.path.exists(os.path.join(root, ref)):
                fail(f"{os.path.relpath(manifest, root)}: referenced path {ref} does not exist")


def frontmatter(path):
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("\"'")
    return None


def check_skills(root):
    skill_files = glob.glob(os.path.join(root, ".agents", "skills", "*", "SKILL.md")) + glob.glob(
        os.path.join(root, "community", "*", "SKILL.md")
    )
    for base in (os.path.join(root, ".agents", "skills"), os.path.join(root, "community")):
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            folder = os.path.join(base, entry)
            if os.path.isdir(folder) and not os.path.isfile(os.path.join(folder, "SKILL.md")):
                fail(f"{os.path.relpath(folder, root)}: skill folder has no SKILL.md")
    for path in skill_files:
        rel = os.path.relpath(path, root)
        fields = frontmatter(path)
        if fields is None:
            fail(f"{rel}: missing or unterminated --- frontmatter")
            continue
        for key in ("name", "description"):
            if not fields.get(key):
                fail(f"{rel}: frontmatter has no {key}")
        folder = os.path.basename(os.path.dirname(path))
        if fields.get("name") and fields["name"] != folder:
            fail(f"{rel}: name '{fields['name']}' does not match its folder '{folder}'")


def check_symlinks(root):
    for path in walk_files(root):
        if os.path.islink(path):
            fail(f"{os.path.relpath(path, root)}: symlinks are not allowed")


def check_mirror_state(root, parsed):
    state_path = os.path.join(root, ".mirror-state.json")
    if not os.path.isfile(state_path):
        fail(".mirror-state.json is missing; the official paths have never been synced")
        return
    state = parsed.get(state_path)
    recorded = state.get("managed_hash") if isinstance(state, dict) else None
    if not isinstance(recorded, str) or not recorded:
        fail(".mirror-state.json: needs a managed_hash string")
        return
    actual = managed_hash(root, MANAGED_PATHS)
    if actual != recorded:
        fail(
            ".mirror-state.json: managed paths changed since the last sync "
            f"(recorded {recorded[:12]}, found {actual[:12]}). Official paths are "
            "synced from Flaim's main codebase; see CONTRIBUTING.md."
        )


def main():
    args = sys.argv[1:]
    check_state = "--check-mirror-state" in args
    args = [arg for arg in args if arg != "--check-mirror-state"]
    root = os.path.abspath(args[0] if args else ".")
    parsed = check_json(root)
    check_manifest_paths(root, parsed)
    check_skills(root)
    check_symlinks(root)
    if check_state:
        check_mirror_state(root, parsed)
    if errors:
        for message in errors:
            print(f"error: {message}")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
