import os
import time
import json
import subprocess as sp
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

CURRENT_DIR = os.path.dirname(__file__)
STATE_DIR = os.path.join(CURRENT_DIR, "../data/state")
LOG_DIR = os.path.join(CURRENT_DIR, "../log")
LOG_FILE_PATH = os.path.join(LOG_DIR, f"appium.log")

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def start_appium_server(config):
    ip_address = config['appium_server']['ip_address']
    port = config['appium_server']['port']
    # Run Appium server, store logfile
    appium_service = AppiumService()
    appium_service.start(args=[
        '--address', ip_address,
        '-p', port,
        '--log', LOG_DIR,
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
    print(os.listdir(STATE_DIR))
    for f in os.listdir(STATE_DIR): # 如果os.listdir下的文件都是.开头的
        if f.startswith(".") and f != ".gitkeep":
            os.remove(os.path.join(STATE_DIR, f)) # 删除文件
    if not os.listdir(STATE_DIR) or os.listdir(STATE_DIR) == [".gitkeep"]:
        capture_screenshot(driver, os.path.join(STATE_DIR, f"{time.time()}.png"))
    try:
        while True:
            current_page_source = get_current_page_source(driver)
            if current_page_source != previous_page_source:
                screenshot_path = os.path.join(STATE_DIR, f"{time.time()}.png")
                capture_screenshot(driver, screenshot_path)
                previous_page_source = current_page_source
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Exiting the loop.")
    finally:
        driver.quit()


if __name__ == "__main__":
    config = read_config(os.path.join(CURRENT_DIR, 'config.json'))
    main(config)