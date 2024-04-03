import requests
import argparse
import pprint
import json
import re


def generate_codename(text):
    # Convert text to lowercase
    text = text.lower()

    # Replace spaces with underscores
    text = text.replace(" ", "_")

    # Remove all non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9_]', '', text)

    return text


parser = argparse.ArgumentParser(description='Get StartGG data for a game')
parser.add_argument('game_id', type=int, help='StartGG Videogame ID')
parser.add_argument("-t", "--tsh", action="store_true",
                    help="Print data in TSH config format")
args = parser.parse_args()

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
            "gameId": args.game_id
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

if args.tsh:
    new_data = {}

    for c in data.get("characters"):
        pass

    new_data["stage_to_codename"] = {}

    for s in data.get("stages"):
        new_data["stage_to_codename"][s["name"]] = {
            "smashgg_id": s["id"],
            "codename": generate_codename(s["name"])
        }

    data = new_data

json_string = json.dumps(data, indent=4)
print(json_string)
