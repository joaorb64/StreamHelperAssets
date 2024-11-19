import json
from copy import deepcopy
from glob import glob
from datetime import datetime

# Define the base directory
base_dir = './games/'
list_config_paths = glob(f"{base_dir}/*/*/config.json")
for path in glob(f"{base_dir}/*/*/*/config.json"):
    list_config_paths.append(path)
for config_path in list_config_paths:
    with open(config_path, "rt", encoding="utf-8") as config_file:
        config_json = json.loads(config_file.read())

    now_time = datetime.utcnow()
    minor = int(now_time.hour)*3600 + int(now_time.minute)*60 + int(now_time.second)
    calver = now_time.strftime('%y.%m.%d') + "." + str(minor)

    config_json["version"] = calver
    

    with open(config_path, "wt", encoding="utf-8") as config_file:
        config_file.write(json.dumps(config_json, indent=2))
