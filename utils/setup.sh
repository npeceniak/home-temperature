#!/bin/bash

WORKING_DIR="$(dirname "${BASH_SOURCE[0]}")"

# echo $WORKING_DIR

cd $WORKING_DIR

python3 -m venv venv

source venv/bin/activate
python -m pip install -r ./requirements.txt

cd ..

echo "Clearing old files from pico"
rshell rm -rf /pyboard

echo "Uploading files to Pico"
rshell cp -r ./lib/phew/phew/. ./src/* /pyboard/

rshell repl pyboard import main