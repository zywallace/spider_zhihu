#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Build-in / Std
import os, platform, random
import re, json, cookielib

# requirements
import requests, termcolor

def download_captcha():
    url = "http://www.zhihu.com/captcha.gif"
    r = requests.get(url, params={"r": random.random()} )
    if int(r.status_code) != 200:
        raise NetworkError(u"验证码请求失败")
    image_name = u"verify." + r.headers['content-type'].split("/")[1]
    open( image_name, "wb").write(r.content)
    """
        System platform: https://docs.python.org/2/library/platform.html
    """
    Logging.info(u"正在调用外部程序渲染验证码 ... ")
    if platform.system() == "Linux":
        Logging.info(u"Command: xdg-open %s &" % image_name )
        os.system("xdg-open %s &" % image_name )
    elif platform.system() == "Darwin":
        Logging.info(u"Command: open %s &" % image_name )
        os.system("open %s &" % image_name )
    elif platform.system() == "SunOS":
        os.system("open %s &" % image_name )
    elif platform.system() == "FreeBSD":
        os.system("open %s &" % image_name )
    elif platform.system() == "Unix":
        os.system("open %s &" % image_name )
    elif platform.system() == "OpenBSD":
        os.system("open %s &" % image_name )
    elif platform.system() == "NetBSD":
        os.system("open %s &" % image_name )
    elif platform.system() == "Windows":
        os.system("open %s &" % image_name )
    else:
        Logging.info(u"我们无法探测你的作业系统，请自行打开验证码 %s 文件，并输入验证码。" % os.path.join(os.getcwd(), image_name) )

    captcha_code = raw_input( termcolor.colored("请输入验证码: ", "cyan") )
    return captcha_code

def search_xsrf():
    url = "http://www.zhihu.com/"
    r = requests.get(url)
    if int(r.status_code) != 200:
        print(u"验证码请求失败")
    results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
    if len(results) < 1:
        print(u"提取XSRF 代码失败" )
        return None
    return results[0]

def build_form(account, password):
    form = {"email": account, "password": password, "remember_me": True }

    form['_xsrf'] = search_xsrf()
    form['captcha'] = download_captcha()
    return form

def upload_form(form):
    url = "http://www.zhihu.com/login/email"

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "http://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }

    r = requests.post(url, data=form, headers=headers)
    if int(r.status_code) != 200:
        raise (u"表单上传失败!")

    if r.headers['content-type'].lower() == "application/json":
        try:
            # 修正  justkg 提出的问题: https://github.com/egrcc/zhihu-python/issues/30
            result = json.loads(r.content)
        except Exception as e:
            print e
            result = {}
        if result["r"] == 0:
            print (u"登录成功")
            return {"result": True}
        elif result["r"] == 1:
            print (u"登录失败！")
            return {"error": {"code": int(result['errcode']), "message": result['msg'], "data": result['data'] } }
        else:
            print (u"表单上传出现未知错误: \n \t %s )" % ( str(result) ) )
            return {"error": {"code": -1, "message": u"unknow error"} }
    else:
        print "error"
        return {"error": {"code": -2, "message": u"parse error"} }


def islogin():
    # check session
    url = "http://www.zhihu.com"
    r = requests.get(url, allow_redirects=False)
    status_code = int(r.status_code)
    if status_code == 301 or status_code == 302:
        # 未登录
        return False
    elif status_code == 200:
        return True
    else:
        print(u"网络故障")
        return None


def read_account_from_config_file(config_file="config.ini"):
    # NOTE: The ConfigParser module has been renamed to configparser in Python 3.
    #       The 2to3 tool will automatically adapt imports when converting your sources to Python 3.
    #       https://docs.python.org/2/library/configparser.html
    from ConfigParser import ConfigParser
    cf = ConfigParser()
    if os.path.exists(config_file) and os.path.isfile(config_file):
        print(u"正在加载配置文件 ...")
        cf.read(config_file)

        email = cf.get("info", "email")
        password = cf.get("info", "password")
        if email == "" or password == "":
            print(u"帐号信息无效")
            return (None, None)
        else: return (email, password)
    else:
        print(u"配置文件加载失败！")
        return (None, None)


def login(account=None, password=None):
    if islogin() == True:
        print(u"你已经登录过咯")
        return True

    if account == None:
        (account, password) = read_account_from_config_file()
    if account == None:
        account  = raw_input("请输入登录帐号: ")
        password = raw_input("请输入登录密码: ")


    form_data = build_form(account, password)

    result = upload_form(form_data)
    if "error" in result:
        if result["error"]['code'] == 1991829:
            # 验证码错误
            print(u"验证码输入错误，请准备重新输入。" )
            return login()
        else:
            print(u"unknow error." )
            return False
    elif "result" in result and result['result'] == True:
        # 登录成功
        print(u"登录成功！" )
        requests.cookies.save()
        return True

if __name__ == "__main__":

    s = requests.Session()
    s.cookies = cookielib.LWPCookieJar('cookies')
    s.cookies.load(ignore_discard=True)
    login()
