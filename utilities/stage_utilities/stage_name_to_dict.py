import os
import json

listdir = os.listdir('./')

stage_dict = {}

for file in listdir:
    if file.endswith('.png'):
        codename = file.replace(".png", "")
        stage_dict[codename]={
            "codename": codename
        }

print (json.dumps(stage_dict, sort_keys=True))