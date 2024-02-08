import requests
import argparse
import pprint
import json
import xmltodict
from collections import defaultdict
import math
import magic
import re

tsh_config = json.load(
    open("/home/joao/StreamHelperAssets/games/ssbu/base_files/config.json"))

codenames = [c["codename"]
             for c in tsh_config["character_to_codename"].values()]

smashdata = xmltodict.parse(open("/home/joao/Download/test.xml").read())

out = defaultdict(lambda: defaultdict(lambda: defaultdict()))

for entry in smashdata["struct"]["list"]["struct"]:
    hashobj = None

    for h in entry["hash40"]:
        if h["@hash"] == "ui_chara_id":
            hashobj = h["#text"]
            break

    hashobj_id = None

    for h in entry["hash40"]:
        if h["@hash"] == "ui_layout_id":
            hashobj_id = h["#text"]
            break

    codename_id = hashobj.split("ui_chara_")[1]

    codename = codename_id
    base_id = int(hashobj_id.rsplit("_", 1)[1])

    if codename == "flame_first":
        codename = "eflame"

    if codename not in codenames:
        print(f"Invalid {codename}")
        continue

    if hashobj:
        print(f"== {codename} (base {base_id}) ==")

    data = {e["@hash"]: e["#text"] for e in entry["float"]}
    data.update({e["@hash"]: e["#text"] for e in entry["byte"]})

    inner_id = 0

    while True:
        global_id = base_id + inner_id

        attrs = [
            f"chara_1_{2}_scale",
            f"chara_1_{2}_offset_x",
            f"chara_1_{2}_offset_y"
        ]

        if attrs[0] not in data:
            break

        out[codename][global_id]["scale"] = float(data[attrs[0]])
        out[codename][global_id]["offset_x"] = int(data[attrs[1]])
        out[codename][global_id]["offset_y"] = int(data[attrs[2]])

        eyecount = int(data["eye_2_flash_count"])

        eyex = []
        eyey = []

        for e in range(eyecount):
            eyex.append(
                int(data[f"eye_2_flash{e}_pos_x"]))
            eyey.append(
                int(data[f"eye_2_flash{e}_pos_y"]))

        try:
            t = magic.from_file(
                f'/home/joao/StreamHelperAssets/games/ssbu/full/chara_1_{codename}_0{global_id}.png')
            w, h = re.search(r'(\d+) x (\d+)', t).groups()
        except:
            w = 256
            h = 256

        out[codename][global_id]["x"] = \
            int(w)/2.0 \
            - out[codename][global_id]["offset_x"] * 1.0/out[codename][global_id]["scale"] \
            + sum(eyex)/len(eyex) * 1.0/out[codename][global_id]["scale"]

        out[codename][global_id]["y"] = \
            int(h)/2.0 \
            + out[codename][global_id]["offset_y"] * 1.0/out[codename][global_id]["scale"] \
            - sum(eyey)/len(eyey) * 1.0/out[codename][global_id]["scale"]

        print("eyecount", eyecount)

        inner_id += 1
        break

out2 = {
    "eyesights": {},
    "rescaling_factor": {}
}

for codename, data in out.items():
    if not codename in out2["rescaling_factor"]:
        out2["rescaling_factor"][codename] = {}

    if not codename in out2["eyesights"]:
        out2["eyesights"][codename] = {}

    for skin_id, skin_data in data.items():
        out2["eyesights"][codename][skin_id] = {
            "x": int(skin_data["x"]),  # * float(skin_data["scale"]),
            "y": int(skin_data["y"]),  # * float(skin_data["scale"]),
        }
        out2["rescaling_factor"][codename][skin_id] = float(skin_data["scale"])

for codename, d in out2["eyesights"].items():
    data = out2["eyesights"][codename]
    zoomData = out2["rescaling_factor"][codename]

    if len(data) > 1:
        for skin in data.values():
            allEqual = True

            if str(data[0]) != str(skin):
                allEqual = False
                break

        if allEqual:
            print(codename)

        if codename in [
            "ike",
            "ptrainer",
            "murabito",
            "wiifit",
            "reflet",
            "cloud",
            "kamui",
            "bayonetta",
            "inkling",
            "master",
            "demon"
        ]:
            data[3] = data[1]
            data[5] = data[1]
            data[7] = data[1]
            zoomData[3] = zoomData[1]
            zoomData[5] = zoomData[1]
            zoomData[7] = zoomData[1]

        if codename in [
            "brave",
            "trail"
        ]:
            data[4] = data[0]
            data[5] = data[1]
            data[6] = data[2]
            data[7] = data[3]
            zoomData[4] = zoomData[0]
            zoomData[5] = zoomData[1]
            zoomData[6] = zoomData[2]
            zoomData[7] = zoomData[3]
            print(data)

        if codename in [
            "jack",
            "edge"
        ]:
            data[7] = data[6]
            zoomData[7] = zoomData[6]

        if codename in [
            "miifighter",
            "miiswordsman",
            "miigunner"
        ]:
            data.pop(1)
            data.pop(7)
            zoomData.pop(1)
            zoomData.pop(7)

        if codename == "pikmin":
            data[5] = data[4]
            data[6] = data[4]
            data[7] = data[4]
            zoomData[5] = zoomData[4]
            zoomData[6] = zoomData[4]
            zoomData[7] = zoomData[4]

out2["eyesights"].pop("random")
out2["rescaling_factor"].pop("random")

pprint.pp(out2)

full_config = json.load(
    open("/home/joao/StreamHelperAssets/games/ssbu/full/config.json"))

full_config["eyesights"] = out2["eyesights"]
full_config["rescaling_factor"] = out2["rescaling_factor"]

with open("/home/joao/StreamHelperAssets/games/ssbu/full/config.json", 'w') as outfile:
    json.dump(full_config, outfile, sort_keys=True, indent=2)
