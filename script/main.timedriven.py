from appium import webdriver
import subprocess as sp
import time
from datetime import datetime
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
    print("appium is listening : ", appium_service.is_listening)

    return ip_address, port

def initialize_driver(ip_address, port):
    options = UiAutomator2Options()
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "13",
        "deviceName": "Android Emulator",
        "appPackage": "com.google.android.calculator",
        "appActivity": "com.android.calculator2.Calculator"
    }
    options.set_capability('appium:chromeOptions', desired_caps)

    # appium 1-->2: no need to add /wd/hub to the end of the url
    # appium 2: no slash at the end of the url
    driver = webdriver.Remote(
        command_executor='http://{}:{}'.format(ip_address, port), 
        options=options
    )

    print("appium is connected to the device")
    return driver

def get_current_page_source(driver):
    current_time = time.time()
    xml_string = driver.page_source
    xml_path = f'../data/xml/{current_time}.appium.xml'
    with open(xml_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_string)
    img_path = f'../data/img/{current_time}.appium.png'
    driver.get_screenshot_as_file(img_path)   

def main():
    ip_address, port = start_appium_server()
    driver = initialize_driver(ip_address, port)

    try:
        while True:
            # 如果用户对页面进行了任何的操作,就会触发
            get_current_page_source(driver) # 获取当前页面的 XML 结构
            time.sleep(5)

    except KeyboardInterrupt:
        # 捕获 Ctrl+C 信号，退出循环
        print("Exiting the loop.")
    finally:
        # 关闭 Appium 会话
        driver.quit()

if __name__ == "__main__":
    main()