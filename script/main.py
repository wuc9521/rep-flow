from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

options = UiAutomator2Options()

_options = {}
_options['platformName'] = 'Android'
_options['platformVersion'] = '13'
_options['deviceName'] = 'Android Emulator'
_options['appPackage'] = 'tv.danmaku.bili'
_options['appActivity'] = '.MainActivityV2'
_options['automationName'] = 'UiAutomator2'
_options['language'] = 'en'
_options['locale'] = 'US'
_options['noReset'] = True
options.set_capability('appium:chromeOptions', {'w3c': False})

# capabilities = dict( 
#     platformName='Android',
#     automationName='UiAutomator2',
#     deviceName='emulator-5554',
#     appPackage='tv.danmaku.bili',
#     appActivity='.MainActivityV2',
#     language='en',
#     locale='US',
#     noReset=True
# )

# Appium 服务器地址
server = 'http://127.0.0.1:4723/wd/hub'
driver = webdriver.Remote(
    command_executor=server,
    options=options,
)


# 获取当前页面的 XML 结构
def get_current_page_source():
    xml_string = driver.page_source
    xml_path = f'./fetch/screenshot_{time.time()}.xml'
    with open(xml_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_string)
    print(f'Page source saved to: {xml_path}')

# 在这里监听用户点击事件
# 这只是一个示例，具体实现会依赖于你的设备和操作系统
# 你可能需要使用第三方库或工具来监听设备的输入事件

# 等待一段时间，保持脚本运行
time.sleep(30)

# 获取当前页面的 XML 结构
get_current_page_source()

# 关闭 Appium 会话
driver.quit()
