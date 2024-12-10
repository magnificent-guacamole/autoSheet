PYTHON_SCRIPT = main.py
SECRETS_EXPORT_FILE = secrets.export
VENV_DIR = venv

all: run

$(VENV_DIR)/bin/activate: 
	python3 -m venv $(VENV_DIR) && \
	. $(VENV_DIR)/bin/activate && \
	python3 -m pip install helium

run: $(VENV_DIR)/bin/activate
	. $(VENV_DIR)/bin/activate && \
	. ./$(SECRETS_EXPORT_FILE) && \
	./$(PYTHON_SCRIPT) -t -f

compile: $(VENV_DIR)/bin/activate
	. $(VENV_DIR)/bin/activate && \
	python -m py_compile $(PYTHON_SCRIPT)

clean:
	@echo "Deleting $(VENV_DIR) and whipping $(SECRETS_EXPORT_FILE)"
	@rm -rf $(VENV_DIR)
	@echo "" > $(SECRETS_EXPORT_FILE)
