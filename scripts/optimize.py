"""
Losslessly optimizes the PNGs added or modified since the last processed commit.
"""
import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from asset_changes import load_changes


def optimize(filename):
    result = subprocess.run(
        ["optipng", "-quiet", "-strip", "all", filename],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Failed to optimize {filename}: {result.stderr.strip()}")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changes", required=True)
    args = parser.parse_args()

    filenames = [
        f["path"] for f in load_changes(args.changes)["files"]
        if f["status"] in ("A", "M")
        and f["path"].lower().endswith(".png")
        and os.path.isfile(f["path"])
    ]

    print(f"Optimizing {len(filenames)} images")
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        failures = sum(1 for code in executor.map(optimize, filenames) if code)

    print(f"Done, {failures} failures")


if __name__ == "__main__":
    main()
