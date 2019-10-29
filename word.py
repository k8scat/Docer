# -*- coding: utf-8 -*-

"""
@author: hsowan <hsowan.me@gmail.com>
@date: 2019/10/28

爬取稻壳网站上的word

"""
import json
import os
import re
import time

from pymongo import MongoClient
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import sqlite3

docer_home = 'https://www.docer.com/'
cookies_file = 'cookies.json'

# 开启mongodb
# mongo_uri = 'mongodb://root:root@localhost:27017/'
# mongo_db = 'docer'
# collection_name = 'word'

# Todo: 使用sqlite
sqlite_db = 'docer.db'

# 保存爬取文件的绝对路径
save_path = '/Users/mac/Downloads/docer/word/'


def download(download_url):
    # Selenium 如何使用webdriver下载文件（chrome浏览器）: https://blog.csdn.net/weixin_41812940/article/details/82423892
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_settings.popups': 0,
        'download.default_directory': save_path,
    }
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('w3c', False)
    # d = DesiredCapabilities.CHROME
    # d['loggingPrefs'] = {'performance': 'ALL'}
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}
    executable_path = os.path.abspath('chromedriver')
    driver = webdriver.Chrome(executable_path=executable_path, options=options, desired_capabilities=caps)

    try:
        # 先请求，再添加cookies
        # selenium.common.exceptions.InvalidCookieDomainException: Message: Document is cookie-averse
        driver.get(docer_home)
        # 从文件中获取到cookies
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.loads(f.read())
        for c in cookies:
            driver.add_cookie({'name': c['name'], 'value': c['value'], 'path': c['path'], 'domain': c['domain'],
                               'secure': c['secure']})
        driver.get(download_url)
        sleep(1)
        # 获取word名称
        word_name = driver.find_element_by_xpath("/html/body/div[@id='__nuxt']/div[@id='__layout']/div[@id='App']/div[@class='g-router-regular']/div[2]/div[@class='preview g-clearfloat']/div[@class='preview__info']/h1[@class='preview__title']").text
        # 只要简历模板
        if word_name.find('简历') == -1:
            return

        # 获取word编号
        pattern = re.compile(r'\d+')
        word_id = pattern.findall(driver.find_element_by_xpath("/html/body/div[@id='__nuxt']/div[@id='__layout']/div[@id='App']/div[@class='g-router-regular']/div[2]/div[@class='preview g-clearfloat']/div[@class='preview__info']/ul[@class='preview__detail g-clearfloat']/li[@class='preview__detail-item'][3]").text)[0]

        # 是否是VIP模板
        is_vip = driver.find_element_by_xpath("/html/body/div[@id='__nuxt']/div[@id='__layout']/div[@id='App']/div[@class='g-router-regular']/div[2]/div[@class='preview g-clearfloat']/div[@class='preview__info']/ul[@class='preview__detail g-clearfloat']/li[@class='preview__detail-item'][4]").text.find('VIP') != -1
        # 只爬取VIP模板
        if not is_vip:
            return

        # 开启mongodb
        # 使用mongodb保存文件信息
        # if col.find_one({'id': word_id}):
        #     return
        # else:
        #     col.insert_one(dict(name=word_name, id=word_id, url=url))

        # Todo: 使用sqlite代替mongodb

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH,
             "/html/body/div[@id='__nuxt']/div[@id='__layout']/div[@id='App']/div[@class='g-router-regular']/div[2]/div[@class='preview g-clearfloat']/div[@class='preview__info']/div[@class='preview__btns g-clearfloat']/span[2]"))
        )
        # 解决: element not interactable
        sleep(1)
        element.click()
        # 等待下载完成以及网络日志
        sleep(7)

        # 对下载文件进行重命名
        logs = driver.get_log('performance')
        for log in logs:
            if log['level'] == 'INFO':
                json_message = json.loads(log['message'])
                if json_message['message']['method'] == 'Network.requestWillBeSent':
                    resource_uri = json_message['message']['params']['documentURL']
                    if resource_uri and resource_uri.count('file.cache.docer.com') == 1:
                        # 对资源路径进行分割获取下载文件名
                        s = resource_uri.split('/')
                        filename = s[len(s) - 1]
                        # 下载文件名后缀
                        filename_suffix = filename.split('.')[1]
                        # 如果存在同名文件则对文件名进行处理: 原有文件名-时间戳.文件名后缀
                        save_filename = word_name + '-' + str(int(time.time())) if os.path.exists(f'{save_path + word_name + "." + filename_suffix}') else word_name

                        cmd = f'mv {save_path + filename} {save_path + save_filename + "." + filename_suffix}'
                        os.system(cmd)
                        break

    finally:
        driver.quit()


if __name__ == '__main__':
    base_url = 'https://www.docer.com/s/wps/?page='

    for i in range(1, 314):
        url = base_url + str(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Host': 'www.docer.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

        # 开启mongodb
        # client = MongoClient(mongo_uri)
        # db = client[mongo_db]
        # col = db[collection_name]

        # Todo: 使用sqlite代替mongodb

        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                html = r.content.decode()
                soup = BeautifulSoup(html, 'lxml')
                items = soup.select('ul.m-list.g-justify-list.sub-wps-container li a')
                for item in items:
                    word_uri = 'https:' + item['href']
                    download(word_uri)

        finally:
            # client.close()
            pass
