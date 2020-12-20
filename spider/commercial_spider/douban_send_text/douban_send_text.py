import time
from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from urllib.parse import urlencode, quote
import requests

username = '15716302402'
password = 'jyw83139200..'


class Douban():

    def __init__(self, username, password, keyword, title, content):
        self.group = []
        self.username = username
        self.password = password
        self.keyword = keyword
        self.title = title
        self.content = content
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        print(111)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.get("https://www.douban.com/")
        self.login()
        self.get_keyword_group()

    def login(self):
        sleep(30)

    def get_keyword_group(self):
        for key in self.keyword:
            self.group = self.get_group(key)
            self.send_all()

    def get_group(self, key):
        self.browser.get("https://www.douban.com/search?cat=1019&q={}".format(quote(key)))
        self.browser.find_element_by_class_name('inp-btn').click()
        self.browser.implicitly_wait(5)
        try:
            self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/ul/li[5]/a').click()
            self.browser.implicitly_wait(2)
        except:
            print("error")
            pass
        self.browser.implicitly_wait(2)
        try:
            for i in range(5):
                self.browser.find_element_by_class_name('result-list-ft').click()
                self.browser.implicitly_wait(5)
        except NoSuchElementException:
            pass
        regex = """href="https://www.douban.com/link2/(.+?)\""""
        temp_group = re.findall(re.compile(regex), self.browser.page_source)
        for i in temp_group:
            self.group.append("https://www.douban.com/link2/{}".format(i))
        print("一共有{}个小组".format(len(self.group)))
        self.group = list(set(self.group))
        return self.group
        # print(self.group)

    def send_all(self):
        for url in self.group:
            self.send_per_group(url)

    def send_per_group(self, url):
        # print(url)
        sleep(90)
        self.browser.get(url)
        self.browser.implicitly_wait(2)
        # 查找加入小组按钮
        try:
            self.browser.find_element_by_class_name('group-misc').click()
            self.browser.implicitly_wait(3)
        except Exception:
            print("找不到加入小组按钮")
            pass
        # 查找发言链接
        try:
            self.browser.find_element_by_class_name('bns').click()
            self.browser.implicitly_wait(3)
        except Exception:
            print("找不到发言按钮")
            pass
        # 发帖
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="group-editor-root"]/div/div[2]/div[1]/span/textarea').send_keys(self.title)
        except Exception:
            print("定位标题位置出错")
            pass
        # try:
        #     self.browser.find_element_by_xpath('//*[@id="group-editor-root"]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/div/span/span').send_keys(self.content)
        # except NoSuchElementException:
        #     print("send text error")
        #     pass
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="group-editor-root"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/div').send_keys(
                self.content)
            self.browser.find_element_by_xpath('//*[@id="nav-top-actions"]/div/div/a[2]').click()
            sleep(2)
            print("发帖成功")
        except Exception:
            print("send image error")
            pass


if __name__ == '__main__':
    keyword = ["java",  "编程",  "人工智能", "算法", "前端", "后端", "大数据", "深度学习", "机器学习"]
    title = """【腾讯云】11.11 云上盛惠，云产品限时抢购，1核2G云服务器首年88"""
    content = """【腾讯云】11.11 云上盛惠，云产品限时抢购，1核2G云服务器首年88元
https://curl.qcloud.com/MY56qqvc"""
    for key in keyword:
        douban = Douban(username, password, keyword, title, content)
        douban.browser.close()
