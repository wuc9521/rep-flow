from appium import webdriver
import subprocess as sp
import time
from datetime import datetime
from appium.options.android import UiAutomator2Options
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


print("appium is connected to the device")  # Nothing is printed, the script

def get_current_page_source():
    xml_string = driver.page_source
    xml_path = f'./xml/{time.time()}.appium.xml'
    with open(xml_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_string)
    print(f'Page source saved to: {xml_path}')


# 等待一段时间，保持脚本运行
time.sleep(10)

# 获取当前页面的 XML 结构
get_current_page_source()

# 关闭 Appium 会话
driver.quit()
