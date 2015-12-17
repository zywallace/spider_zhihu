#-*- coding:utf-8 -*-

# Build-in / Std
import sys,cookielib

# requirements
import requests
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup

# module
from login import islogin,Logging
from user import User
from question import Question

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


