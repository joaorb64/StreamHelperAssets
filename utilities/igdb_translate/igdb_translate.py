import json
from pathlib import Path
from igdb.wrapper import IGDBWrapper
from glob import glob


with open("credentials.json", 'rt', encoding="utf-8") as file:
    credentials = json.loads(file.read())
    wrapper = IGDBWrapper(credentials.get("client_id"), credentials.get("app_access_token"))

region_request = wrapper.api_request('regions', f'fields identifier, name, category; offset 0;')
region_json = json.loads(region_request)
region_mapping = {
    "ja-JP": ["ja"],
    "ko-KR": ["ko"],
    "EU": ["fr", "it", "de", "nl", "es", "pt_PT", "en_UK", "en_IE"],
    "EU_oppose": ["es_LA", "fr_CA"]
}

games_glob = "../../games/*/base_files/config.json"
games_config_paths = glob(games_glob)
for config_path in games_config_paths:
    with open(config_path, 'rt', encoding="utf-8") as config_file:
        config = json.loads(config_file.read())
    current_locales = config.get("locale", {})
    game_name = config.get("name")
    igdb_slug = config.get("igdb_game_id")
    if igdb_slug:
        game_request = wrapper.api_request('games', f'fields id, name, game_localizations; offset 0; where slug="{igdb_slug}";')
        game_json = json.loads(game_request)
        game_id = game_json[0].get("id")
        localizations_request = wrapper.api_request('game_localizations', f'fields name, region, game; offset 0; where game={game_id};')
        for localization in json.loads(localizations_request):
            if localization.get("name"):
                print(localization.get("name"))
                region_id = localization.get("region")
                for region in region_json:
                    if region_id == region.get("id") and localization.get("name").lower() != game_name.lower():
                        region_slug = region.get("identifier")
                        for locale in region_mapping.get(region_slug, []):
                            current_locale_data = current_locales.get(locale)
                            if current_locale_data:
                                if not current_locale_data.get("name"):
                                    current_locales[locale]["name"] = localization.get("name")
                            else:
                                current_locales[locale] = {"name": localization.get("name")}
                        if region_slug == "EU":
                            for locale in region_mapping.get("EU_oppose", []):
                                current_locale_data = current_locales.get(locale)
                                if current_locale_data:
                                    if not current_locale_data.get("name"):
                                        current_locales[locale]["name"] = game_name
                                else:
                                    current_locales[locale] = {"name": game_name}

        if current_locales:
            config["locale"] = current_locales

        with open(config_path, 'wt', encoding="utf-8") as config_file:
            config_file.write(json.dumps(config, indent=2))
