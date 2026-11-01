"""
Publishes asset archives to the rolling "latest" GitHub release, which TSH
downloads from (releases/latest/download/<name>).

  upload  Uploads (replacing) the given archives, then checks that every file
          referenced by assets.json exists in the release.
  prune   Deletes archives from the release that assets.json no longer
          references (removed packs, or volumes of a pack that shrank).

Needs the gh CLI with GH_TOKEN and GITHUB_REPOSITORY set.
"""
import argparse
import json
import os
import subprocess
import sys
import time

REPO = os.environ.get("GITHUB_REPOSITORY", "joaorb64/StreamHelperAssets")
UPLOAD_BATCH = 10


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def latest_release():
    release = json.loads(gh("api", f"repos/{REPO}/releases/latest"))
    return release["id"], release["tag_name"]


def release_assets(release_id):
    pages = gh("api", "--paginate", "--slurp",
               f"repos/{REPO}/releases/{release_id}/assets?per_page=100")
    return {a["name"]: a["id"] for page in json.loads(pages) for a in page}


def expected_assets():
    with open("assets.json", "r", encoding="utf-8") as f:
        assets = json.load(f)
    return {
        name
        for game in assets.values()
        for pack in game["assets"].values()
        for name in pack["files"]
    }


def upload(tag, release_id, archives):
    for i in range(0, len(archives), UPLOAD_BATCH):
        batch = archives[i:i + UPLOAD_BATCH]
        for attempt in range(1, 4):
            print(f"Uploading {batch} (attempt {attempt})")
            result = subprocess.run(
                ["gh", "release", "upload", tag, *batch, "--clobber", "--repo", REPO])
            if result.returncode == 0:
                break
            time.sleep(10 * attempt)
        else:
            sys.exit(f"Failed to upload {batch}")

    missing = sorted(expected_assets() - set(release_assets(release_id)))
    if missing:
        sys.exit(f"Release {tag} is missing files referenced by assets.json: {missing}")
    print(f"Release {tag} has every file referenced by assets.json")


def prune(release_id, max_deletions):
    expected = expected_assets()
    orphans = sorted(
        (name, asset_id) for name, asset_id in release_assets(release_id).items()
        if ".7z" in name and name not in expected
    )
    if len(orphans) > max_deletions:
        sys.exit(f"Refusing to delete {len(orphans)} release files (limit {max_deletions}): "
                 f"{[name for name, _ in orphans]}")
    for name, asset_id in orphans:
        print(f"Deleting orphaned release file {name}")
        gh("api", "-X", "DELETE", f"repos/{REPO}/releases/assets/{asset_id}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    upload_parser = sub.add_parser("upload")
    upload_parser.add_argument("--archives", required=True,
                               help="File listing archive paths to upload")
    prune_parser = sub.add_parser("prune")
    prune_parser.add_argument("--max-deletions", type=int, default=25)
    args = parser.parse_args()

    release_id, tag = latest_release()
    print(f"Publishing to release {tag}")

    if args.command == "upload":
        with open(args.archives, "r", encoding="utf-8") as f:
            archives = [line.strip() for line in f if line.strip()]
        upload(tag, release_id, archives)
    else:
        prune(release_id, args.max_deletions)


if __name__ == "__main__":
    main()
