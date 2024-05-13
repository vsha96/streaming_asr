.PHONY: install run

# Define the environment directory
ENV_DIR := ./env

install:
	# Create a virtual environment
	python3 -m venv $(ENV_DIR)
	# Activate the virtual environment and install packages from requirements.txt
	$(ENV_DIR)/bin/pip install --upgrade pip
	$(ENV_DIR)/bin/pip install -r requirements.txt

run: install
	# Run the main.py script using the virtual environment
	$(ENV_DIR)/bin/python main.py