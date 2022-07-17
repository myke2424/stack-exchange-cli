VENV_PATH=.stack-exchange-venv
VENV_PYTHON_BIN=${VENV_PATH}/bin/python3.10
VENV_PIP_BIN=${VIRTUALENV_PATH}/bin/pip
REQUIREMENTS_FILE_PATH=./requirements.txt

all: create_venv install_requirements

create_venv:
	@echo "Creating venv..."
	python3.10 -m venv "${VENV_PATH}"
	@echo "Done!"

install_requirements:
	@echo "Installing requirements..."
	${VENV_PYTHON_BIN} -m pip install --upgrade pip
	${VENV_PYTHON_BIN} -m pip install -r "${REQUIREMENTS_FILE_PATH}"
	@echo "Done!"

.PHONY: all