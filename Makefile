.PHONY: build clean help lint run
.DEFAULT_GOAL := help

VENV_NAME = venv
PYTHON = ${VENV_NAME}/bin/python3
PY_FILES= find . -type f -name '*.py' ! -path './venv/*' 2> /dev/null

black: venv
	black -v `${PY_FILES}`
	@echo ""

build: venv
	pyinstaller --onefile \
		--distpath ./build \
		--workpath ./tmp \
		--name minij \
		src/main.py

clean:
	rm -rfv ./tmp ./build ./*.spec ./*.egg-info

flake8: venv
	flake8 `${PY_FILES}`
	@echo ""

help:
	@echo "---------------------HELP------------------------"
	@echo "To build the project type make build"
	@echo "To clean the project type make clean"
	@echo "To lint the project type make lint"
	@echo "To run the project type make run (only for dev)"
	@echo "-------------------------------------------------"

isort: venv
	isort `${PY_FILES}`
	@echo ""

lint: black isort flake8

run: venv
	${PYTHON} src/main.py

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate

