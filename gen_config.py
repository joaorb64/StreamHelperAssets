#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import os
from posix import listdir
import sys
import tarfile

list = {}

games = [f for f in os.listdir("./games/") if os.path.isdir("./games/"+f)]

for game in games:
    print("Game: "+game)
    path = "./games/"+game+"/"

    try:
        with open(path+"config.json", 'r', encoding='utf-8') as configFile:
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
        path = "./games/"+game+"/"+assetDir+"/"

        try:
            with open(path+"config.json", 'r', encoding='utf-8') as configFile:
                config = json.load(configFile)
                list[game]["assets"][assetDir] = {
                    "name": config.get("name"),
                    "credits": config.get("credits")
                }
                # with tarfile.open("./games/"+game+"/"+assetDir+".tar.gz", "w:gz") as tar:
                #     tar.add(path, arcname=assetDir)
        except Exception as e:
            print(e)

with open('assets.json', 'w') as outfile:
    json.dump(list, outfile, indent=4, sort_keys=True)