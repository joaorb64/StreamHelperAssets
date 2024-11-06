import requests
import json
import os
import traceback

# Define the base directory
base_dir = './games/'

out = open("startgg_insights.md", "w", encoding="utf-8")


def log(text: str):
    out.write(text+"\n")
    print(text)


def get_game_data(game_id):
    data = requests.post(
        "https://www.start.gg/api/-/gql",
        headers={
            "client-version": "20",
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
        },
        json={
            "operationName": "VideogameData",
            "variables": {
                "gameId": game_id
            },
            "query":
                '''
                    query VideogameData($gameId: Int!) {
                        videogame(id: $gameId, slug: $gameSlug) {
                            id
                            characters {
                                id
                                name
                            }
                            stages {
                                id
                                name
                            }
                        }
                    }
                '''
        }
    )
    data = json.loads(data.text)
    data = data.get("data", {}).get("videogame", {})
    return data


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        files.sort()
        if 'config.json' in files:
            # Skip updating config.json if it is directly in the base_files directory
            if not root.endswith("base_files"):
                continue

            config_path = os.path.join(root, 'config.json')

            with open(config_path, 'r', encoding='utf-8') as config_file:
                config_data = json.load(config_file)

            if config_data.get("smashgg_game_id"):
                log(f"## {config_data['name']}")

                try:
                    game_data = get_game_data(
                        config_data.get("smashgg_game_id"))

                    if game_data.get("characters"):
                        sgg_characterNames = [
                            c["name"] for c in game_data["characters"]
                        ]

                        for k, v in config_data.get("character_to_codename").items():
                            if v.get("smashgg_name") and v.get("smashgg_name") not in sgg_characterNames:
                                log(
                                    f"- Character [{k}]: Character name [{v['smashgg_name']}] doesn\'t exist in StartGG")

                        tsh_characterNames = [
                            c["smashgg_name"] for c in config_data.get("character_to_codename").values() if "smashgg_name" in c
                        ]

                        coverage = 0

                        for c in sgg_characterNames:
                            if c not in tsh_characterNames:
                                log(f"- Character [{c}] not assigned in TSH!")
                            else:
                                coverage += 1

                        log(
                            f"### Coverage: ({coverage}/{len(sgg_characterNames)})")
                    else:
                        log(
                            "Game has no characters in startgg...? Or do we have a wrong game id?")
                except:
                    log(traceback.format_exc())

            log("")


process_directory(base_dir)

out.close()
