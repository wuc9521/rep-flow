from appium import webdriver
import subprocess as sp
from datetime import datetime
from appium.webdriver.appium_service import AppiumService

ip_address = '127.0.0.1'
port = '4725'
date = datetime.now().strftime("%Y%m%d%H%M")

# Run Appium server, store logfile
appium_service = AppiumService()
appium_service.start(args=[
    '--address', ip_address,
    '-p', port,
    '--log-timestamp',
    '--log', './logs/{}.appium.log'.format(date),
], stdout=sp.DEVNULL)

print("appium is running : ", appium_service.is_running)  # return True, ok
print("appium is listening : ", appium_service.is_listening)  # return True, ok

desired_caps = {
    "platformName": "Android",
    "platformVersion": "13",
    "deviceName": "Android Emulator",
    "appPackage": "com.google.android.calculator",
    "appActivity": "com.android.calculator2.Calculator"
}


driver = webdriver.Remote(
    command_executor='http://{}:{}/wd/hub'.format(ip_address, port),
    desired_capabilities=desired_caps
)

print("appium is connected to the device")  # Nothing is printed, the script
