#!/bin/bash
set -x
set -o errexit
pipenv install -r requirements.txt
pipenv run python get_icons_from_inkipedia.py
pipenv run python update_old_config.py
pipenv run python add_modes_to_stages.py
pipenv run python get_tableturf_art.py
