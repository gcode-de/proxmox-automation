#!/usr/bin/env python3
"""Embed the shared icon CSS in both configs; no third-party dependencies."""
import argparse
import base64
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if configs need regeneration")
    args = parser.parse_args()
    url = "data:text/css;base64," + base64.b64encode(
        (ROOT / "homer-category-icons.css").read_bytes()
    ).decode("ascii")
    updates = []
    for kind in ("local", "remote"):
        path = ROOT / f"homer-config_{kind}.yml"
        original = path.read_text(encoding="utf-8")
        pattern = r'(?m)^  - "data:text/css;base64,[A-Za-z0-9+/=]+"$'
        updated, count = re.subn(pattern, lambda _: f'  - "{url}"', original)
        if count != 1:
            raise SystemExit(f"{path.name}: expected exactly one embedded stylesheet, got {count}")
        updates.append((path, original, updated))
    stale = [path.name for path, old, new in updates if old != new]
    if args.check:
        if stale:
            raise SystemExit("Regenerate embedded CSS: " + ", ".join(stale))
        print("Both embedded stylesheets match homer-category-icons.css")
    else:
        for path, old, new in updates:
            if old != new:
                path.write_text(new, encoding="utf-8")
        print("Both embedded stylesheets are current")

if __name__ == "__main__":
    main()
