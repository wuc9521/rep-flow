import time
import subprocess as sp
from appium import webdriver
from datetime import datetime
from appium.common.logger import logger
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

def start_appium_server():
    ip_address = '127.0.0.1'
    port = '4725'
    date = datetime.now().strftime("%Y%m%d%H%M")

    # Run Appium server, store logfile
    appium_service = AppiumService()
    appium_service.start(args=[
        '--address', ip_address,
        '-p', port,
        '--log-timestamp',
        '--log', './log/{}.appium.log'.format(date),
        '--use-plugins='.format("images"),
    ], stdout=sp.DEVNULL)
    print("appium is running : ", appium_service.is_running)
    return ip_address, port


def initialize_driver(ip_address, port):
    options = UiAutomator2Options()
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "13",
        "deviceName": "Android Emulator",
    }
    options.set_capability('appium:chromeOptions', desired_caps)

    # appium 1-->2: no need to add /wd/hub to the end of the url
    # appium 2: no slash at the end of the url
    driver = webdriver.Remote(
        command_executor='http://{}:{}'.format(ip_address, port),
        options=options,
    ),

    print("appium connected to the device")
    return driver


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
    
def main():
    ip_address, port = start_appium_server()
    driver = initialize_driver(ip_address, port)
    driver = driver[0]
    previous_page_source = get_current_page_source(driver)
    try:
        while True:
            current_page_source = get_current_page_source(driver)
            if current_page_source != previous_page_source:
                screenshot_path = f'../data/img/{time.time()}.png'
                capture_screenshot(driver, screenshot_path)
                previous_page_source = current_page_source
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting the loop.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()