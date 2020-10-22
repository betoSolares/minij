.PHONY: build clean help lint
.DEFAULT_GOAL := help

VENV_NAME = venv
PYTHON = ${VENV_NAME}/bin/python3
PY_FILES= find . -type f -name '*.py' ! -path './venv/*' 2> /dev/null

brunette: venv
	brunette `${PY_FILES}` --config=setup.cfg
	@echo ""

build: venv
	pyinstaller --onefile \
		--distpath ./build \
		--workpath ./tmp \
		--name minij \
		--add-data 'docs/ParsingTable.xlsx:docs' \
		--hidden-import pyexcel \
		--hidden-import pyexcel.plugins.renderers.excel \
		--hidden-import pyexcel.plugins.renderers._texttable \
		--hidden-import pyexcel.plugins.parsers.excel \
		--hidden-import pyexcel.plugins.sources.http \
		--hidden-import pyexcel.plugins.sources.file_input \
		--hidden-import pyexcel.plugins.sources.memory_input \
		--hidden-import pyexcel.plugins.sources.file_output \
		--hidden-import pyexcel.plugins.sources.output_to_memory \
		--hidden-import pyexcel.plugins.sources.pydata.bookdict \
		--hidden-import pyexcel.plugins.sources.pydata.dictsource \
		--hidden-import pyexcel.plugins.sources.pydata.arraysource \
		--hidden-import pyexcel.plugins.sources.pydata.records \
		--hidden-import pyexcel_io \
		--hidden-import pyexcel_io.readers \
		--hidden-import pyexcel_io.writers \
		--hidden-import pyexcel_io.database \
		--hidden-import pyexcel_io \
		--hidden-import pyexcel_ods \
		--hidden-import pyexcel_ods.odsw \
		--hidden-import pyexcel_xlsx \
		--hidden-import pyexcel_xlsx.xlsxw \
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
	@echo "-------------------------------------------------"

isort: venv
	isort `${PY_FILES}`
	@echo ""

lint: brunette isort flake8

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate

