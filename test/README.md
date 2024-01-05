# README

perform random test(monkey) on android app, collect screenshots and logs

downgrade python client if unable to connect to appium server
```
pip install Appium-Python-Client==1.2.0
```

the base path of the screenshot is /test/screenshot

# reproduce bugs and catch screenshots
cd to /script
python random_test.py

# reference

[adb monkey](https://developer.android.com/studio/test/other-testing-tools/monkey)
