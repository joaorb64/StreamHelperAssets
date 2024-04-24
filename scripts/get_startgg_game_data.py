import requests
import argparse
import pprint
import json

parser = argparse.ArgumentParser(description='Get StartGG data for a game')
parser.add_argument('game_id', type=int, help='StartGG Videogame ID')
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
pprint.pprint(json.loads(data.text))
