import json
import collections

eyesights_dict = {"Crewmate": {}}

for index in range(25):
    eyesights_dict["Crewmate"][index] = {"x": 0, "y": 0}

eyesights_dict = collections.OrderedDict(sorted(eyesights_dict.items()))

with open("eyesights.json", "wt", encoding="utf-8") as eyesights_file:
    eyesights_file.write(json.dumps({"eyesights": eyesights_dict}, indent=2))
