#-*- coding:utf-8 -*-

# Build-in / Std
import os, sys, time, platform, random
import re, json, cookielib

# requirements
import requests, termcolor, html2text
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup

# module
from login import islogin
from login import Logging


"""
    Note:
        1. 身份验证由 `auth.py` 完成。
        2. 身份信息保存在当前目录的 `cookies` 文件中。
        3. `requests` 对象可以直接使用，身份信息已经自动加载。

    By Luozijun (https://github.com/LuoZijun), 09/09 2015

"""
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")


if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")

reload(sys)
sys.setdefaultencoding('utf8')

#方法有查看名称\简介\关注人数
class topic:
    topic_url = None
    # session = None
    soup = None
    updated_time = None

    def __init__(self, topic_url):
        if topic_url[0:26] != "http://www.zhihu.com/topic":
            raise ValueError("\"" + topic_url + "\"" + " : it isn't a topic url.")
        else:
            self.topic_url = topic_url


    def parser(self):
        if self.topic_url != None:
            r = requests.get(self.topic_url)
            soup = BeautifulSoup(r.content)
            self.soup = soup
            self.updated_time = time.localtime(time.time())

    def topic_title(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        topic_title = soup.find("div", class_="topic-name") \
            .find("h1").string.encode("utf-8")
        return topic_title
#关注的人数

    def desc(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        topic_desc = soup.find("div", id="zh-topic-desc") \
            .find("div").string.encode("utf-8")
        return topic_desc

    def followers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        num = soup.find("a", href="/topic/19553732/followers") \
            .find("strong").string.encode("utf-8")
        return num

    def top_answerer(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        name = soup.find_all("div",class_="zm-topic-side-person-item-content")
        name = name.a