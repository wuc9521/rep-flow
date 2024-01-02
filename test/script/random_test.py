import random
from test_scripts import YourTestCase
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

if __name__ == '__main__':
    
    capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.android.settings',
    appActivity='.Settings',
    language='en',
    locale='US'
    )

    appium_server_url = 'http://localhost:4723'

    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    # Get all test methods in the test case
    test_methods = [method for method in dir(YourTestCase) if callable(getattr(YourTestCase, method)) and method.startswith('test_')]
    print(f'Test methods: {test_methods}')
    test_class = YourTestCase(driver)
    test_class.take_screenshot('{}_init.png'.format(test_class.counter))

    # Run tests randomly in a loop
    for _ in range(5):
        random_test_method = random.choice(test_methods)
        my_method = getattr(test_class, random_test_method, None)
        my_method()
