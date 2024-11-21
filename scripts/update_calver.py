import json
from copy import deepcopy
from glob import glob
from datetime import datetime
import os
import subprocess

FILE_DIR = os.path.dirname(__file__)


def run_linux_command(command: str):
    """
        Runs Linux command
    """
    try:
        print(f">> {command}")
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Ensure output is in text mode
            check=False
        )

        # Extract the exit code, stdout, and stderr from the completed process
        exit_code = result.returncode
        stdout_output = result.stdout.strip()
        stderr_output = result.stderr.strip()

        # Return the results as a tuple
        return exit_code, stdout_output, stderr_output
    except Exception as e:
        # If an error occurs during the execution, return an error tuple
        return -1, '', str(e)

_, CURRENT_TAG, _ = run_linux_command("git describe --tags --always")

LATEST_TAG = None
with open(f"{FILE_DIR}/last_tag.txt", "r", encoding="utf-8") as f:
    LATEST_TAG = f.read().strip()
_, LIST_CHANGED_FILES, _ = run_linux_command(f"git diff-tree --name-only {LATEST_TAG} {CURRENT_TAG} -r")
# _, LIST_CHANGED_FILES, _ = run_linux_command(f"git diff --name-only {LATEST_TAG} head")
print(LIST_CHANGED_FILES)

list_config_paths = []
for line in LIST_CHANGED_FILES.splitlines():
    if line.startswith("games/"):
        dir_name = "/".join(line.split("/")[:-1])
        config_path = f"{dir_name}/config.json"
        if (config_path not in list_config_paths) and (os.path.isfile(config_path)):
            print(f"Detected change in pack {dir_name}")
            list_config_paths.append(config_path)
        if "base_files" in dir_name:
            while not dir_name.endswith("base_files"):
                dir_name = "/".join(dir_name.split("/")[:-1])
                config_path = f"{dir_name}/config.json"
                if (config_path not in list_config_paths) and (os.path.isfile(config_path)):
                    print(f"Detected change in pack {dir_name}")
                    list_config_paths.append(config_path)


for config_path in list_config_paths:
    with open(config_path, "rt", encoding="utf-8") as config_file:
        config_json = json.loads(config_file.read())

    now_time = datetime.utcnow()
    minor = int(now_time.hour)*3600 + int(now_time.minute)*60 + int(now_time.second)
    calver = now_time.strftime('%y.%m.%d') + "." + str(minor)

    config_json["version"] = calver

    with open(config_path, "wt", encoding="utf-8") as config_file:
        config_file.write(json.dumps(config_json, indent=2))
