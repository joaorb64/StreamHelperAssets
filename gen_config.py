#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from genericpath import isfile
import json
import os
from posix import listdir
import sys
import tarfile
import subprocess

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

    deleteOldZips = subprocess.Popen(
        ["rm "+path+"*.7z*"],
        shell=True
    )
    deleteOldZips.communicate()

    list[game]["assets"]["config"] = {
        "name": "Base config for "+config.get("name"),
        "credits": "",
        "description": "Needed in order to use this game",
        "version": config.get("version"),
        "files": {
            "config.json": {
                "name": "config.json",
                "size": os.path.getsize(path+"config.json")
            }
        }
    }

    for assetDir in assetDirs:
        path = "./games/"+game+"/"+assetDir+"/"

        try:
            with open(path+"config.json", 'r', encoding='utf-8') as configFile:
                config = json.load(configFile)
                
                _zip = subprocess.Popen([
                    "7z", "-v80m", "-r", "a",
                    "./games/"+game+"/"+assetDir+".7z",
                    "./games/"+game+"/"+assetDir
                ])
                result = _zip.communicate()

                fileNames = [f for f in os.listdir("./games/"+game+"/") if f.startswith(assetDir+".7z")]
                files = {}
                for f in fileNames:
                    files[f] = {
                        "name": f,
                        "size": os.path.getsize("./games/"+game+"/"+f)
                    }

                list[game]["assets"][assetDir] = {
                    "name": config.get("name"),
                    "credits": config.get("credits"),
                    "description": config.get("description"),
                    "files": files,
                    "version": config.get("version")
                }

                with open(path+"README.md", 'w', encoding='utf-8') as readme:
                    readme.write("# "+config.get("name")+"\n")
                    readme.write(config.get("description")+"\n")
                    readme.write("Credits: "+config.get("credits")+"\n")
        except Exception as e:
            print(e)

with open('assets.json', 'w') as outfile:
    json.dump(list, outfile, indent=4, sort_keys=True)