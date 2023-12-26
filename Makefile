PYTHON = python3
PIP = pip3
NPM = npm

OS := $(shell uname)


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
	$(PIP) install -r requirements.txt

run: clean
	@$(PYTHON) utils/detect.py
	@nohup $(PYTHON) app.py >/dev/null 2>&1 &
	@echo "App is running..."
	@nohup $(PYTHON) script/main.py >/dev/null 2>&1 &
	@echo "Script is running..."
	@echo "Please open http://localhost:5000"
	@sleep 1.2
ifeq ($(OS),Linux)
	@xdg-open http://localhost:5000 
else
ifeq ($(OS),Darwin)
	@open http://localhost:5000
endif
endif

clean: stop
ifeq ($(OS),Linux)
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
ifeq ($(OS),Darwin)
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
	@del /Q data\state\*.png
	@rd /Q log\*.log
endif
endif

stop:
ifeq ($(OS),Linux)
	-@if pgrep -f 'app.py' > /dev/null; then \
		echo "Stop running app..."; \
		pkill -f 'app.py'; \
		echo "Stopped."; \
	fi
	-@if pgrep -f 'main.py' > /dev/null; then \
		echo "Stop running script..."; \
		pkill -f 'main.py'; \
		echo "Stopped."; \
	fi
else
ifeq ($(OS),Darwin)
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
