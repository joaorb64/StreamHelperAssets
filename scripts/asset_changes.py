"""
Works out which files and asset packs changed between the last processed
commit (scripts/last_tag.txt) and HEAD.

Run as a script to write the result to a JSON file that the other build
scripts read with load_changes(). Only tree objects are compared, so this
works in a blobless (--filter=blob:none) clone without downloading any assets.
"""
import argparse
import json
import os
import subprocess

FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def git(*args):
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def pack_of(path):
    """games/<game>/<pack>/... -> games/<game>/<pack>, or None."""
    parts = path.split("/")
    if len(parts) >= 4 and parts[0] == "games":
        return "/".join(parts[:3])
    return None


def load_changes(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True,
                        help="Where to write the changes JSON")
    parser.add_argument("--sparse-patterns",
                        help="Also write sparse-checkout patterns for the changed packs here")
    args = parser.parse_args()

    with open(os.path.join(FILE_DIR, "last_tag.txt"), "r", encoding="utf-8") as f:
        base = f.read().strip()
    head = git("rev-parse", "HEAD")

    print(f"Comparing last processed commit ({base}) -> HEAD ({head})")

    # check=True: a missing base commit must fail loudly instead of silently
    # reporting "no changes".
    diff = git("diff-tree", "-r", "--no-renames", "--name-status", base, head)

    files = []
    packs = set()
    for line in diff.splitlines():
        status, path = line.split("\t", 1)
        files.append({"status": status, "path": path})
        pack = pack_of(path)
        if pack:
            packs.add(pack)

    packs = sorted(packs)
    has_png = any(
        f["status"] in ("A", "M") and f["path"].lower().endswith(".png")
        for f in files
    )

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump({"base": base, "head": head, "files": files,
                  "packs": packs}, f, indent=2)

    if args.sparse_patterns:
        with open(args.sparse_patterns, "w", encoding="utf-8") as f:
            f.writelines(f"/{pack}/\n" for pack in packs)

    print(f"{len(files)} changed files in {len(packs)} packs")
    for pack in packs:
        print(f"  {pack}")

    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"has_changes={'true' if packs else 'false'}\n")
            f.write(f"has_png={'true' if has_png else 'false'}\n")


if __name__ == "__main__":
    main()
