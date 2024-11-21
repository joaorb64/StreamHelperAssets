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

LAST_TAG = None
with open(f"{FILE_DIR}/last_tag.txt", "r", encoding="utf-8") as f:
    LAST_TAG = f.read().strip()

changed_files = run_linux_command(
    f"git diff-tree --no-commit-id --name-status {LAST_TAG} {CURRENT_TAG} -r")

print(
    f"Comparing last processed commit ({LAST_TAG}) -> origin/main ({CURRENT_TAG})")

if not CURRENT_TAG or not LAST_TAG:
    exit(1)

print(changed_files)

changes = []

for line in changed_files[1].splitlines():
    line = line.strip()
    print(line)
    if ".png" in line:
        split = line.split("\t")
        change = split[0].strip()
        filename = split[1].strip()

        print(change, filename)

        if change in ['A', 'M']:
            changes.append(change)

for i, change in enumerate(changes):
    print(f"Optimizing [{i+1}/{len(changes)}]")
    run_linux_command(f"optipng {filename} -strip all")

