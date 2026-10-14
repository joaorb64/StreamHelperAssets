#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the 7z archives of asset packs and regenerates assets.json.

Only packs listed in --changes (or missing from the current assets.json) are
rebuilt; the rest keep their existing archive entries. --full rebuilds all.
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(FILE_DIR, "scripts"))

from asset_changes import load_changes  # noqa: E402


def build_archive(game, assetDir, delete_sources):
    gamePath = f"./games/{game}/"
    archivePrefix = f"{game}.{assetDir}.7z"

    for stale in glob.glob(gamePath + archivePrefix + "*"):
        os.remove(stale)

    # PNGs are already compressed: a fast LZMA2 level gives nearly the same
    # size in a fraction of the time. py7zr in TSH reads any level.
    result = subprocess.run([
        "7z", "a", "-v1500m", "-r", "-mx=1", "-mmt=on", "-bso0", "-bsp0",
        gamePath + archivePrefix,
        gamePath + assetDir
    ])
    if result.returncode != 0:
        raise RuntimeError(
            f"7z failed for {game}/{assetDir} (exit code {result.returncode})")

    files = {}
    for f in sorted(os.listdir(gamePath)):
        if f.startswith(archivePrefix):
            files[f] = {
                "name": f,
                "size": os.path.getsize(gamePath + f)
            }

    if delete_sources:
        # Frees disk space during full rebuilds
        for png in glob.glob(f"{gamePath}{assetDir}/*.png"):
            os.remove(png)

    print(f"Built {game}/{assetDir}: {list(files)}")
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changes",
                        help="Changes JSON from scripts/asset_changes.py")
    parser.add_argument("--full", action="store_true",
                        help="Rebuild every pack")
    parser.add_argument("--delete-sources", action="store_true",
                        help="Delete pack PNGs after archiving them")
    parser.add_argument("--archives-out",
                        help="Write the paths of built archives here")
    args = parser.parse_args()

    if not args.full and not args.changes:
        parser.error("either --changes or --full is required")

    changedPacks = set(load_changes(args.changes)[
                       "packs"]) if args.changes else set()

    with open("assets.json", 'r', encoding='utf-8') as oldAssetsFile:
        oldAssets = json.load(oldAssetsFile)

    list_ = {}
    lastVersions = {}
    toBuild = []
    errors = []

    games = sorted(f for f in os.listdir("./games/")
                   if os.path.isdir("./games/" + f))

    for game in games:
        try:
            path = "./games/" + game + "/"

            with open(path + "base_files/config.json", 'r', encoding='utf-8') as configFile:
                gameConfig = json.load(configFile)
            list_[game] = {
                "name": gameConfig["name"],
                "assets": {}
            }

            assetDirs = sorted(
                f for f in os.listdir(path) if os.path.isdir(path + f))

            for assetDir in assetDirs:
                with open(path + assetDir + "/config.json", 'r', encoding='utf-8') as configFile:
                    config = json.load(configFile)

                eyesightData = config.get("eyesights", {})

                if assetDir == "base_files":
                    with open(path + assetDir + "/icon/config.json", 'r', encoding='utf-8') as iconConfig:
                        sub_config = json.load(iconConfig)
                        eyesightData = sub_config.get("eyesights", {})

                oldFiles = oldAssets.get(game, {}).get(
                    "assets", {}).get(assetDir, {}).get("files")

                if args.full or f"games/{game}/{assetDir}" in changedPacks or not oldFiles:
                    toBuild.append((game, assetDir))

                list_[game]["assets"][assetDir] = {
                    "name": config.get("name"),
                    "credits": config.get("credits"),
                    "description": config.get("description"),
                    "files": oldFiles or {},
                    "version": config.get("version"),
                    "has_stage_data": len(config.get("stage_to_codename", {})) > 0,
                    "has_eyesight_data": len(eyesightData) > 0
                }
                lastVersions[f'{game}.{assetDir}'] = config.get("version", 0)

        except Exception:
            errors.append(game)
            print(f"Error reading game {game}")
            print(traceback.format_exc())

    print(f"Building {len(toBuild)} archives")

    builtArchives = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(build_archive, game, assetDir, args.delete_sources): (game, assetDir)
            for game, assetDir in toBuild
        }
        for future, (game, assetDir) in futures.items():
            try:
                files = future.result()
                list_[game]["assets"][assetDir]["files"] = files
                builtArchives.extend(
                    f"games/{game}/{name}" for name in files)
            except Exception:
                errors.append(f"{game}/{assetDir}")
                print(traceback.format_exc())

    if errors:
        # Writing assets.json now would drop these packs for every user
        print(f"Failed: {errors}")
        sys.exit(1)

    with open('assets.json', 'w', encoding="utf-8") as outfile:
        json.dump(list_, outfile, indent=4, sort_keys=True)

    with open('last_versions.json', 'w', encoding="utf-8") as outfile:
        json.dump(lastVersions, outfile, indent=4, sort_keys=True)

    current_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    with open(f"{FILE_DIR}/scripts/last_tag.txt", "w", encoding="utf-8") as f:
        f.write(current_commit)

    if args.archives_out:
        with open(args.archives_out, "w", encoding="utf-8") as f:
            f.writelines(f"{a}\n" for a in builtArchives)


if __name__ == "__main__":
    main()
