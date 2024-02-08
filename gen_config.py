#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from genericpath import isfile
import json
import os
from posix import listdir
import sys
import tarfile
import subprocess
import time
import traceback
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--destroy", action="store_true",
    help="Destructive method where it deletes the original image files. Made for the online pipeline."
)
parser.add_argument(
    "-t", "--tag",
    help="Github release tag"
)
args = parser.parse_args()

list = {}

games = [f for f in os.listdir("./games/") if os.path.isdir("./games/"+f)]

oldAssets = {}

with open("assets.json", 'r', encoding='utf-8') as oldAssetsFile:
    oldAssets = json.load(oldAssetsFile)

lastVersions = {}

# with open("last_versions.json", 'r', encoding='utf-8') as lastVersionsFile:
#     lastVersions = json.load(lastVersionsFile)

for game in games:
    print("Game: "+game)
    path = "./games/"+game+"/"

    try:
        with open(path+"/base_files/config.json", 'r', encoding='utf-8') as configFile:
            config = json.load(configFile)
            list[game] = {
                "name": config["name"],
                "assets": {}
            }
    except Exception as e:
        print(e)
        continue

    assetDirs = [f for f in os.listdir(path) if os.path.isdir(path+f)]
    print("Assets: "+str(assetDirs))

    for assetDir in assetDirs:
        assetPath = "./games/"+game+"/"+assetDir+"/"

        modified = True if float(config.get("version", 0)) > float(
            lastVersions.get(f'{game}.{assetDir}', 0)) else False

        lastVersions[f'{game}.{assetDir}'] = config.get("version", 0)

        if modified:
            deleteOldZips = subprocess.Popen(
                ["rm "+path+"/"+assetDir+".7z*"],
                shell=True
            )
            deleteOldZips.communicate()

        print(">"+assetPath)
        print("Was modified", modified)

        try:
            with open(assetPath+"config.json", 'r', encoding='utf-8') as configFile:
                config = json.load(configFile)

                files = {}

                if modified:
                    _zip = subprocess.Popen([
                        "7z", "-v1500m", "-r", "a",
                        "./games/"+game+"/"+game+"."+assetDir+".7z",
                        "./games/"+game+"/"+assetDir
                    ])
                    result = _zip.communicate()

                    fileNames = [f for f in os.listdir(
                        "./games/"+game+"/") if f.startswith(game+"."+assetDir+".7z")]
                    for f in fileNames:
                        files[f] = {
                            "name": f,
                            "size": os.path.getsize("./games/"+game+"/"+f)
                        }

                        # Upload 7z to release
                        print(f"> Upload ./games/{game}/{f}")

                        print(
                            f"/usr/bin/hub release edit -a {args.tag} ./games/{game}/{f}")

                        _upload = subprocess.Popen(
                            [f"/usr/bin/hub release edit -a {args.tag} ./games/{game}/{f}"], shell=True)
                        result = _upload.communicate()
                        print(result, _upload.returncode)

                        # Delete 7z file
                        print(f"> Delete ./games/{game}/{f}")

                        _del = subprocess.Popen(
                            [f"rm -rf ./games/{game}/{f}"], shell=True)
                        result = _del.communicate()
                        print(result, _del.returncode)

                    # Delete original files if flag is set
                    if args.destroy:
                        print("> Deleting image files")
                        _del = subprocess.Popen(
                            [f"rm -rf ./games/{game}/{assetDir}/*.png"], shell=True)
                        result = _del.communicate()
                        print(result)
                else:
                    files = oldAssets[game]["assets"][assetDir]["files"]

                eyesightData = config.get("eyesights", {})

                # When we're dealing with base_files,
                # get eyesight data from base_files/icon config file instead
                if assetDir == "base_files":
                    with open("./games/"+game+"/"+assetDir+"/icon/config.json", 'r', encoding='utf-8') as iconConfig:
                        sub_config = json.load(iconConfig)
                        eyesightData = sub_config.get("eyesights", {})

                list[game]["assets"][assetDir] = {
                    "name": config.get("name"),
                    "credits": config.get("credits"),
                    "description": config.get("description"),
                    "files": files,
                    "version": config.get("version"),
                    "has_stage_data": len(config.get("stage_to_codename", {})) > 0,
                    "has_eyesight_data": len(eyesightData) > 0
                }

                with open(assetPath+"README.md", 'w', encoding='utf-8') as readme:
                    readme.write("# "+config.get("name", "")+"\n\n")
                    readme.write("## Description: \n\n" +
                                 config.get("description", "")+"\n\n")
                    readme.write("## Credits: \n\n" +
                                 config.get("credits", "")+"\n\n")
        except Exception as e:
            print(traceback.format_exc())

with open('assets.json', 'w', encoding="utf-8") as outfile:
    json.dump(list, outfile, indent=4, sort_keys=True)

with open('last_versions.json', 'w', encoding="utf-8") as outfile:
    json.dump(lastVersions, outfile, indent=4, sort_keys=True)
