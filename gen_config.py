#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

list_ = {}
games = [f for f in os.listdir("./games/") if os.path.isdir("./games/" + f)]
oldAssets = {}

with open("assets.json", 'r', encoding='utf-8') as oldAssetsFile:
    oldAssets = json.load(oldAssetsFile)

lastVersions = {}
# with open("last_versions.json", 'r', encoding='utf-8') as lastVersionsFile:
#     lastVersions = json.load(lastVersionsFile)


def process_game(game):
    try:
        print("Game: " + game)
        path = "./games/" + game + "/"

        with open(path + "base_files/config.json", 'r', encoding='utf-8') as configFile:
            config = json.load(configFile)
            list_[game] = {
                "name": config["name"],
                "assets": {}
            }

        assetDirs = [f for f in os.listdir(path) if os.path.isdir(path + f)]
        print("Assets: " + str(assetDirs))

        futures = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            for assetDir in assetDirs:
                futures.append(executor.submit(
                    process_asset_dir, game, assetDir, path, config))

        for future in as_completed(futures):
            future.result()

    except Exception as e:
        print(traceback.format_exc())


def process_asset_dir(game, assetDir, path, config):
    try:
        assetPath = "./games/" + game + "/" + assetDir + "/"
        modified = True if float(config.get("version", 0)) > float(
            lastVersions.get(f'{game}.{assetDir}', 0)) else False
        lastVersions[f'{game}.{assetDir}'] = config.get("version", 0)

        # if modified:
        #     delete_old_zips = subprocess.Popen(
        #         ["rm " + path + "/" + assetDir + ".7z*"], shell=True)
        #     delete_old_zips.communicate()

        print(">" + assetPath)
        print("Was modified", modified)

        with open(assetPath + "config.json", 'r', encoding='utf-8') as configFile:
            config = json.load(configFile)
            files = {}

            if modified:
                _zip = subprocess.Popen([
                    "7z", "-v1500m", "-r", "a",
                    "./games/" + game + "/" + game + "." + assetDir + ".7z",
                    "./games/" + game + "/" + assetDir
                ])
                _zip.communicate()

                fileNames = [f for f in os.listdir(
                    "./games/" + game + "/") if f.startswith(game + "." + assetDir + ".7z")]
                for f in fileNames:
                    files[f] = {
                        "name": f,
                        "size": os.path.getsize("./games/" + game + "/" + f)
                    }

                print("> Delete original PNGs")
                delete_original_files = subprocess.Popen(
                    [f"rm ./games/{game}/{assetDir}/*.png"],
                    shell=True,
                    text=True
                )
                out, err = delete_original_files.communicate()
                print(out, err, delete_original_files.returncode)
            else:
                files = oldAssets[game]["assets"][assetDir]["files"]

            eyesightData = config.get("eyesights", {})

            if assetDir == "base_files":
                with open("./games/" + game + "/" + assetDir + "/icon/config.json", 'r', encoding='utf-8') as iconConfig:
                    sub_config = json.load(iconConfig)
                    eyesightData = sub_config.get("eyesights", {})

            list_[game]["assets"][assetDir] = {
                "name": config.get("name"),
                "credits": config.get("credits"),
                "description": config.get("description"),
                "files": files,
                "version": config.get("version"),
                "has_stage_data": len(config.get("stage_to_codename", {})) > 0,
                "has_eyesight_data": len(eyesightData) > 0
            }

            with open(assetPath + "README.md", 'w', encoding='utf-8') as readme:
                readme.write("# " + config.get("name", "") + "\n\n")
                readme.write("## Description: \n\n" +
                             config.get("description", "") + "\n\n")
                readme.write("## Credits: \n\n" +
                             config.get("credits", "") + "\n\n")

    except Exception as e:
        print(traceback.format_exc())


for game in games:
    process_game(game)

with open('assets.json', 'w', encoding="utf-8") as outfile:
    json.dump(list_, outfile, indent=4, sort_keys=True)

with open('last_versions.json', 'w', encoding="utf-8") as outfile:
    json.dump(lastVersions, outfile, indent=4, sort_keys=True)
