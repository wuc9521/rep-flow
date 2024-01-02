import pytest
import os
import time
from selenium.common.exceptions import NoSuchElementException

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction

class YourTestCase():
    def take_screenshot(self, filename):
        screenshot_file_path = os.path.join(self.screenshot_path, filename)
        self.driver.save_screenshot(screenshot_file_path)
        print(f'Screenshot saved to: {screenshot_file_path}')

    def __init__(self, driver, screenshot_path="../screenshot") -> None:
        self.driver = driver
        self.screenshot_path = screenshot_path
        self.counter = 0

    def test_function_1(self):
        print("This is test_function_1")
        self.take_screenshot('{}_1.png'.format(self.counter))
        # el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Animation')
        # action = TouchAction(self.driver)
        # action.tap(el).perform()

    def test_function_2(self):
        print("This is test_function_2")
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
        el.click()
        # el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Battery')
        # action = TouchAction(self.driver)
        # action.tap(el).perform()
        time.sleep(2)
        # TODO: random click
        x = 100
        y = 100
        self.counter += 1
        self.take_screenshot('{}_2_({}, {}).png'.format(self.counter, x, y))

