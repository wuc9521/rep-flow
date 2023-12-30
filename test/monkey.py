from appium import webdriver
# from appium.options.android import UiAutomator2Options # andriod 2
import subprocess
import time
import os

current_directory = os.getcwd()
print(current_directory)

log_file_path = current_directory + '/log/monkey.log'
screenshot_path = current_directory + '/screenshot/'

# Desired Capabilities
desired_caps = {
    'platformName': 'Android',
    'deviceName': 'Android',
    'appPackage': 'com.liuyaoli.myapplication',
    'appActivity': '.MainActivity',
    'automationName': 'UiAutomator2',
    # Add other capabilities as needed
}

# Appium Server URL
appium_server_url = 'http://localhost:4723'

# if andriod 2 ->
# options = UiAutomator2Options()
# cloud_options = {}
# cloud_options['build'] = "build_1"
# cloud_options['name'] = "test_abc"
# options.set_capability('test:options', desired_caps)
# driver = webdriver.Remote(appium_server_url, options=options)
# print("appium connected to the device")

# Start Appium session
driver = webdriver.Remote(command_executor=appium_server_url, desired_capabilities=desired_caps)
print("appium connected to the device")

# Replace "com.android.settings" with the package name of new app
new_app_package = 'com.liuyaoli.myapplication'
event_count = 500
# --pct-touch 50 --pct-motion 50
loop = 0

try: 
    while(True):
        if loop != 0:
            break
        loop += 1
        print(f"Loop: {loop}")
        # Execute ADB command using subprocess for the new app
        # monkey_command = f'adb shell monkey -p {new_app_package} -v {event_count} -throttle 100'
        monkey_command = 'adb shell monkey -p {} -v 500 -throttle 100 2>&1 | tee {} | (while read -r line; do adb exec-out screencap -p > {}/screenshot_${{line// /_}}.png; done)'.format(new_app_package, log_file_path, screenshot_path)
        with open(log_file_path, 'w') as log_file:
            subprocess.run(monkey_command, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print("Monkey test encountered an error. Exiting loop.")

# Close the Appium session
driver.quit()
