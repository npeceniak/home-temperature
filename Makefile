.PHONY: prepare_venv cache build deploy rshell

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
RSHELL=$(VENV_NAME)/bin/rshell

prepare_venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || python3 -m venv venv
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

rshell: prepare_venv
	${RSHELL}

clear_board: prepare_venv
	${RSHELL} rm -rf /pyboard

upload: prepare_venv
	${RSHELL} cp -r ./src/* /pyboard/

run: prepare_venv
	${RSHELL} repl pyboard import main

config:
	${PYTHON} ./utils/config.py

generate_dashboard:
	${PYTHON} ./utils/gen_html.py