import os
import time
import json
import subprocess as sp
from appium import webdriver
from datetime import datetime
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

curent_dir = os.path.dirname(__file__)

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def start_appium_server(config):
    ip_address = config['appium_server']['ip_address']
    port = config['appium_server']['port']
    date = datetime.now().strftime("%Y%m%d%H%M")

    # Run Appium server, store logfile
    appium_service = AppiumService()
    appium_service.start(args=[
        '--address', ip_address,
        '-p', port,
        '--log-timestamp',
        '--log', os.path.join(curent_dir, f'../log/appium.log'),
        '--use-plugins='.format("images"),
    ], stdout=sp.DEVNULL)
    print("appium is running : ", appium_service.is_running)
    return appium_service


def initialize_driver(config):
    options = UiAutomator2Options()
    desired_caps = config['desired_caps']
    options.set_capability('appium:chromeOptions', desired_caps)

    # appium 1-->2: no need to add /wd/hub to the end of the url
    # appium 2: no slash at the end of the url
    appium_server = config['appium_server']
    ip_address = appium_server['ip_address']
    port = appium_server['port']
    driver = webdriver.Remote(
        command_executor='http://{}:{}'.format(ip_address, port),
        options=options,
    ),

    print("appium connected to the device")
    return driver[0]


def get_current_page_source(driver):
    xml_string = driver.page_source
    return xml_string

def capture_screenshot(driver, screenshot_path):
    driver.save_screenshot(screenshot_path)
    print(f'Screenshot saved to: {screenshot_path}')

def is_button_pressed(driver):
    try:
        buttons = driver.find_elements_by_xpath("//Button")
        for button in buttons:
            if button.is_enabled() and button.is_displayed():
                return True
        return False
    except:
        return False
    
def main(config):
    appium_service = start_appium_server(config)
    driver = initialize_driver(config)
    previous_page_source = get_current_page_source(driver)
    try:
        while True:
            current_page_source = get_current_page_source(driver)
            if current_page_source != previous_page_source:
                screenshot_path = os.path.join(curent_dir, "../data/img/", f"{time.time()}.png")
                capture_screenshot(driver, screenshot_path)
                previous_page_source = current_page_source
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Exiting the loop.")
    finally:
        driver.quit()


if __name__ == "__main__":
    config = read_config(os.path.join(curent_dir, 'config.json'))
    main(config)