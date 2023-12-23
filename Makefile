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

stop:
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

reload:
	adb uninstall io.appium.uiautomator2.server.test