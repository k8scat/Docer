# -*- coding: utf-8 -*-

"""
@author: hsowan <hsowan.me@gmail.com>
@date: 2019/10/27

"""
import json
import time

from selenium import webdriver

if __name__ == '__main__':
    login_url = 'https://www.docer.com/'

    driver = webdriver.Chrome()
    try:
        driver.get(login_url)

        # 延迟60秒, 手机扫码登录
        time.sleep(30)

        # 获取到cookies
        cookies = driver.get_cookies()
        with open('cookies.json', 'w') as f:
            f.write(json.dumps(cookies))

    finally:
        driver.close()
