#!/bin/bash
set -x
set -o errexit
python3 -m pipenv install -r requirements.txt
python3 -m pipenv run python get_icons_from_inkipedia.py
python3 -m pipenv run python update_old_config.py
python3 -m pipenv run python add_modes_to_stages.py
python3 -m pipenv run python get_tableturf_art.py
