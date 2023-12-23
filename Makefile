PYTHON = python3
PIP = pip3
NPM = npm

OS := $(shell uname)

install:
	$(NPM) install
	$(PIP) install -r requirements.txt

run: clean
	nohup $(PYTHON) app.py >/dev/null 2>&1 &
	nohup $(PYTHON) script/main.py >/dev/null 2>&1 &
	@echo "Running..."
	@echo "Please open http://127.0.0.1:5000"
	@sleep 1.2
ifeq ($(OS),Linux)
	xdg-open http://localhost:5000 
else
ifeq ($(OS),Darwin)
	open http://localhost:5000
endif
endif

clean: stop
ifeq ($(OS),Linux)
	@if [ -d "data/state" ]; then rm -f data/state/*.png; fi
	@if [ -d "log" ]; then rm -f log/*.log; fi
else
ifeq ($(OS),Darwin)
	@if [ -d "data/state" ]; then rm -f data/state/*.png; fi
	@if [ -d "log" ]; then rm -f log/*.log; fi
else
	@del /Q data\state\*.png
	@rd /Q log\*.log
endif
endif
	@echo "Cleaned up."

stop:
	@echo "Stopp running..."
ifeq ($(OS),Linux)
	-@pkill -f 'app.py'
	-@pkill -f 'main.py'
else
ifeq ($(OS),Darwin)
	-@pkill -f 'app.py'
	-@pkill -f 'main.py'
else
	-@taskkill /F /IM python.exe
endif
endif
	@echo "Stopped."

reload:
	adb uninstall io.appium.uiautomator2.server.test