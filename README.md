# StreamHelperAssets
Character assets for use with [TournamentStreamHelper](https://github.com/joaorb64/TournamentStreamHelper). You can download all assets directly from within the program.

You may also use them in other projects, just be sure to check out the credits on each pack's README. In Releases you'll find direct downloads to 7z files containing the packs.

# Contributing

Each game follows the sctructure:

Given a <GAMECODE> which is a made-up name, usually using the game name's initials. Everything related to this game is under `/games/<GAMECODE>/`.

## Base game config file
  
The file `/base_files/config.json` contains basic definitions for the game:
  - Game Name
  - SmashGG Game Id
  - character_to_codename: maps the official character's name to their name in SmashGG and to a codename in case the files should follow a pre-defined naming convention. For example, Smash Ultimate's game files are named using codenames, so this is a good way of having a naming convention which is the same as the official game files. If there is none, it's good to at least create codenames that avoid special characters like `.`, `/`, `á`, etc.
  - stage_to_codename: maps official stage names to their ids in SmashGG and to file codenames. Same principle as the previous one.
  - Version
  - Description
  - Credits

Inside `/base_files/` I'm also including at least one asset pack for character icons so that they show up on the program's UI. More on asset packs in its own section.

## Assets Packs

Each folder inside `/game/` and inside `/game/base_files/` that has a `config.json` file is considered an asset pack.

The file `config.json` contains basic definitions for the pack:
  - name: Asset Pack name
  - description
  - credits (use `\n` for newlines)
  - version
  - prefix: prefix for the asset names
  - postfix: postfix for the asset names
  - skin_mapping(optional): if this assets pack has scattered files that should map to specific character skins, you can map skin_mapping.character_codename.skin_id→asset_number. For example, if you have an asset specific to all odd/even skins, you should map the odd ones to 0 and the even ones to 1, if applies. A good example for this is `ssbu/webms`
  
### Adding a new game
  
  - Create a `/games/<GAMECODE>` directory, add your `/base_files/config.json`. Add all data you can provide.
  - For SmashGG game/character IDs, use the endpoint https://api.smash.gg/characters. Control+F for a character name that you know that might be unique to the game you're looking for, and go from there. You'll find both their SmashGG names and game ID here.
  - For games with stage striking, you'll need to open a tournament in SmashGG which has stage striking configured, open Chrome dev tools, go to Network tab, and check the requests to compare the selection ID to the displayed text. I do not know other way of doing this.

### Adding a new assets pack

  - Check in `/games/<GAMECODE>/base_files/config.json` the character codenames. Have your files named after the codenames.
  - Check in other assets packs or official sources what is the game's skins orders, if the game has multiple skins per character, so that you follow the same order as other assets packs.
  - Add all data you need in `config.json` inside your assets pack directory.

### Adding eyesight data to an asset pack

  - Check in `/games/<GAMECODE>/base_files/config.json` the character codenames.
  - Open the `config.json` file inside the asset pack directory.
  - Add an `"eyesights"` section to the JSON with the X and Y coordinates of each character's eyesight, usually situated between both eyes. This section of the JSON will look something like this:
```
 "eyesights": {
    "codename1": {
      "0": {
        "x": 462,
        "y": 135
      }
    },
    "codename2": {
      "0": {
        "x": 417,
        "y": 322
      }
    }
  }
```

### Testing

You can build your own structure in your TournamentStreamHelper install so that you can easly test your files and configuration. I'd suggest copying everything from other game for a quicker start!

### README files

Note that you don't need to create any README files or edit the files outside of `/games/`, since for each new commit I have an auto sequence where github creates all extra files such as READMEs and the zips it uploads to the Releases. I create the README just to reassure proper credits to assets packs, which also becomes easly visible in GitHub.

### Questions
  
If you have any questions, please open an issue and I'll get to you as soon as I can!
