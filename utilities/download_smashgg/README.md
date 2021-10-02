# How to get a game's Smash.gg ID to add it to `game_data.json`

1. Find a tournament for the game you want to add on Smash.gg
1. Get the URL to the event featuring the game you want to add. The URL will look like this: `https://smash.gg/tournament/{tournament_name}/event/{event_name}/overview`
1. Remove the `/overview` part and add `api.` between `https://` and `smash.gg`. Your URL should now look like this: `https://api.smash.gg/tournament/{tournament_name}/event/{event_name}`
1. Open your new URL in a web browser or do a GET request on your new URL, and find the key `"videogameId"`. This should give you the Smash.gg game ID for the game you are looking for!