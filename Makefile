PYTHON = python3
PIP = pip3
NPM = npm

OS := $(shell uname)

install:
	$(NPM) install
	$(PIP) install -r requirements.txt

run: clean
	@$(PYTHON) script/detect.py
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
	@if [ -d "data/state" ] && [ "$(ls -A data/state)" ]; then
  		rm -rf data/state/*
	fi
	@if [ -d "log" ] && [ "$(ls -A log)" ]; then 
		rm -f log/*.log; 
	fi
else
ifeq ($(OS),Darwin)
	@if [ -d "data/state" ] && [ "$(ls -A data/state)" ]; then \
		echo "Cleaning data/state..."; \
		rm -rf data/state/*; \
		echo "Cleaned up."; \
	fi
	@if [ -d "log" ] && [ "$(ls -A log)" ]; then \
		echo "Cleaning log..."; \
		rm -f log/*; \
		echo "Cleaned up."; \
	fi
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