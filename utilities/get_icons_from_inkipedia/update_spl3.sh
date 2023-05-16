#!/bin/sh
set -x
set -o errexit
pip install -r requirements.txt
python get_icons_from_inkipedia.py
python update_old_config.py
python add_modes_to_stages.py