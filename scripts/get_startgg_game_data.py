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
        'Content-Type': 'application/json'
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
