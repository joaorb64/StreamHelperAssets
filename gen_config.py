#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from genericpath import isfile
import json
import os
from posix import listdir
import sys
import tarfile
import subprocess
import time
import traceback

list = {}

games = [f for f in os.listdir("./games/") if os.path.isdir("./games/"+f)]

lastModified = 0
with open("last_modified.json", 'r', encoding='utf-8') as modified:
    lastModified = json.load(modified).get("modified", 0)

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

        modified = True if any(x for x in os.listdir(assetPath) if os.path.getmtime(assetPath+"/"+x) > lastModified) else False

        if modified:
            deleteOldZips = subprocess.Popen(
                ["rm "+path+"*"+assetDir+".7z*"],
                shell=True
            )
            deleteOldZips.communicate()

        print(">"+assetPath)

        try:
            with open(assetPath+"config.json", 'r', encoding='utf-8') as configFile:
                config = json.load(configFile)
                
                if modified:
                    _zip = subprocess.Popen([
                        "7z", "-r", "a",
                        "./games/"+game+"/"+game+"."+assetDir+".7z",
                        "./games/"+game+"/"+assetDir
                    ])
                    result = _zip.communicate()

                fileNames = [f for f in os.listdir("./games/"+game+"/") if f.startswith(game+"."+assetDir+".7z")]
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

                with open(assetPath+"README.md", 'w', encoding='utf-8') as readme:
                    readme.write("# "+config.get("name", "")+"\n\n")
                    readme.write("## Description: \n\n"+config.get("description", "")+"\n\n")
                    readme.write("## Credits: \n\n"+config.get("credits", "")+"\n\n")
        except Exception as e:
            print(traceback.format_exc())

with open('assets.json', 'w') as outfile:
    json.dump(list, outfile, indent=4, sort_keys=True)

with open('last_modified.json', 'w') as outfile:
    json.dump({"modified": time.time()}, outfile, indent=4, sort_keys=True)