PYTHON = python3
PIP = pip3
NPM = npm

install:
	$(NPM) install
	$(PIP) install -r requirements.txt

run:
	cd chatbot && $(PYTHON) app.py &
	cd script && $(PYTHON) main.py &