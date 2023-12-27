PIP = pip3
NPM = npm
APPIUM = appium

ifeq ($(OS),Windows_NT)
	PLATFORM := Windows
	PYTHON := python
else
	PYTHON := python3
	ifeq ($(shell uname),Linux)
		PLATFORM := Linux
	endif
	ifeq ($(shell uname),Darwin)
		PLATFORM := Darwin
	endif
endif



# Function to print colored message
define print_message
	@echo "$(1)$(2)$(COLOR_RESET)"
endef

.PHONY: all install run clean stop boot reload

all: help

help:
	@$(PYTHON) utils/help.py

install:
	$(NPM) install
	$(NPM) install -g appium
	$(PIP) install -r requirements.txt
	$(APPIUM) driver install uiautomator2
	$(PYTHON) -m spacy download en_core_web_sm

run: clean
ifeq ($(PLATFORM),Windows)
	@$(PYTHON) .\utils\detect.py
	@start /B $(PYTHON) .\app.py
	@echo "App is running..."
	@start /B $(PYTHON) .\script\main.py
	@echo "Script is running..."
	@echo "Please open http://localhost:5000"
	@timeout /nobreak /t 1 > nul
	@start http://localhost:5000
else
	@$(PYTHON) utils/detect.py
	@nohup $(PYTHON) app.py >/dev/null 2>&1 &
	@echo "App is running..."
	@nohup $(PYTHON) script/main.py >/dev/null 2>&1 &
	@echo "Script is running..."
	@echo "Please open http://localhost:5000"
	@sleep 1.2
ifeq ($(PLATFORM),Linux)
	@xdg-open http://localhost:5000 
else
ifeq ($(PLATFORM),Darwin)
	@open http://localhost:5000
endif
endif
endif

clean: stop
ifeq ($(PLATFORM),Linux)
	@if [[ `ls -A data/state` ]]; then \
		echo "Cleaning data/state..."; \
		rm -rf data/state/*; \
		rm -rf data/state/.DS_Store; \
	fi
	@if [[ `ls -a ./log` ]]; then \
		echo "Cleaning log..."; \
		rm -f log/*; \
		rm -f log/.DS_Store; \
	fi
	@echo "Cleaned up."; 
else
ifeq ($(PLATFORM),Darwin)
	@if [[ `ls -A data/state` ]]; then \
		echo "Cleaning data/state..."; \
		rm -rf data/state/*; \
		rm -rf data/state/.DS_Store; \
	fi
	@if [[ `ls -a ./log` ]]; then \
		echo "Cleaning log..."; \
		rm -f log/*; \
		rm -f log/.DS_Store; \
	fi
	@rm -rf utils/__pycache__
	@echo "Cleaned up."; 
else
	@if not exist data\state\NUL; then \
		echo "Cleaning data/state..."; \
		rd /S /Q data\state; \
	fi
	@if not exist log\NUL; then \
		echo "Cleaning log..."; \
		rd /S /Q log; \
	fi
endif
endif

stop:
ifeq ($(PLATFORM),Linux)
	-@if pgrep app.py > /dev/null; then \
		echo "Stop running app..."; \
		pkill app.py; \
		echo "Stopped."; \
	fi
	-@if pgrep main.py > /dev/null; then \
		echo "Stop running script..."; \
		pkill main.py; \
		echo "Stopped."; \
	fi
else
ifeq ($(PLATFORM),Darwin)
	-@if pgrep -f 'app.py' > /dev/null; then \
		echo "Stop running app..."; \
		pkill -f 'app.py'; \
		echo "Stopped."; \
	fi
	-@if pgrep -f 'main.py' > /dev/null; then \
		echo "Stop running script..."; \
		pkill -f 'script/main.py'; \
		echo "Stopped."; \
	fi
else
	-@if tasklist /FI "IMAGENAME eq app.py" 2>NUL | find /I /N "app.py">NUL; then \
		echo "Stop running app..."; \
		taskkill /F /IM app.py >NUL; \
		echo "Stopped."; \
	fi
	-@if tasklist /FI "IMAGENAME eq script/main.py" 2>NUL | find /I /N "script/main.py">NUL; then \
		echo "Stop running script..."; \
		taskkill /F /IM script/main.py >NUL; \
		echo "Stopped."; \
	fi
endif
endif
	

boot:
	@echo "Booting..."
	@nohup emulator @Pixel-4XL -no-snapshot-load >/dev/null 2>&1 &
	@sleep 5
	@echo "Booted."

reload:
	adb uninstall io.appium.uiautomator2.server.test
