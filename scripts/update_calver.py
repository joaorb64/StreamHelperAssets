"""
Bumps the calver "version" of every config.json on the path of a file changed
since the last processed commit, from the pack root down to the file's folder.
"""
import argparse
import json
import os
from datetime import datetime, timezone

from asset_changes import load_changes, pack_of


def configs_for(path):
    pack = pack_of(path)
    if not pack:
        return []
    configs = []
    dir_parts = path.split("/")[:-1]
    for depth in range(3, len(dir_parts) + 1):
        config_path = "/".join(dir_parts[:depth]) + "/config.json"
        if os.path.isfile(config_path):
            configs.append(config_path)
    return configs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changes", required=True)
    args = parser.parse_args()

    config_paths = sorted({
        config_path
        for f in load_changes(args.changes)["files"]
        for config_path in configs_for(f["path"])
    })

    now_time = datetime.now(timezone.utc)
    minor = now_time.hour*3600 + now_time.minute*60 + now_time.second
    calver = now_time.strftime('%y.%m.%d') + "." + str(minor)

    for config_path in config_paths:
        print(f"Detected change in pack {os.path.dirname(config_path)}")
        with open(config_path, "rt", encoding="utf-8") as config_file:
            config_json = json.loads(config_file.read())

        config_json["version"] = calver

        with open(config_path, "wt", encoding="utf-8") as config_file:
            config_file.write(json.dumps(config_json, indent=2))


if __name__ == "__main__":
    main()
