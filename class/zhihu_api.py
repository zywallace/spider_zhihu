#-*- coding:utf-8 -*-

# Build-in / Std
import sys, time, re, json, cookielib

# requirements
import requests
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup

# module
from login import islogin

requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    print "error???"

if islogin() != True:
    print(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")

reload(sys)
sys.setdefaultencoding('utf8')

def page_exist(url):
    if url != None:
        r = requests.get(url).status_code
        if r == 404:
            return False

    return True


#方法有用户名 关注人数 粉丝数 回答数 提问数 赞同数 感谢数 查看粉丝 查看关注的人
class User:
    user_url = None
    # session = None
    soup = None
    updated_time = None
    def __init__(self, user_url, user_id=None):
        if user_url == None:
            self.user_id = "匿名用户"
        elif user_url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError("\"" + user_url + "\"" + " : it isn't a user url.")
        else:
            self.user_url = user_url


    def parser(self):
        if self.user_url != None:
            r = requests.get(self.user_url)
            soup = BeautifulSoup(r.content)
            self.soup = soup
            self.updated_time = time.localtime(time.time())

    def user_name(self):
        if self.user_url == None:
            return "匿名用户"
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            user_id = soup.find("div", class_="title-section ellipsis") \
                .find("span", class_="name").string.encode("utf-8")
            return user_id
#关注的人数
    def followees_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            followees_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                .find("a").strong.string)
            return int(followees_num)
#粉丝数
    def followers_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            followers_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                .find_all("a")[1].strong.string)
            return int(followers_num)

    def agree_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            agree_num = int(soup.find("span", class_="zm-profile-header-user-agree").strong.string)
            return int(agree_num)

    def thanks_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            thanks_num = int(soup.find("span", class_="zm-profile-header-user-thanks").strong.string)
            return int(thanks_num)

    def asks_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            asks_num = int(soup.find_all("span", class_="num")[0].string)
            return int(asks_num)

    def answers_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            try:
                answers_num = int(soup.find_all("span", class_="num")[1].string)
                return int(answers_num)
            except Exception as e:
                print self.user_url,e
                return 0
    def get_info(self):
        return self.user_name(),self.user_url,self.followees_num(),self.followers_num(),self.thanks_num()\
            ,self.agree_num(),self.asks_num(),self.answers_num()



    def get_followees(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return
        else:
            followees_num = self.followees_num()
            if followees_num == 0:
                return
            else:
                followee_url = self.user_url + "/followees"
                r = requests.get(followee_url)

                soup = BeautifulSoup(r.content)
                for i in xrange((followees_num - 1) / 20 + 1):
                    if i == 0:
                        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
                        for j in xrange(min(followees_num, 20)):
                            yield user_url_list[j].a["href"]
                    else:
                        post_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
                        _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
                        offset = i * 20
                        hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]
                        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
                        data = {
                            '_xsrf': _xsrf,
                            'method': "next",
                            'params': params
                        }
                        header = {
                            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                            'Host': "www.zhihu.com",
                            'Referer': followee_url
                        }

                        r_post = requests.post(post_url, data=data, headers=header)

                        followee_list = r_post.json()["msg"]
                        for j in xrange(min(followees_num - i * 20, 20)):
                            followee_soup = BeautifulSoup(followee_list[j])
                            user_link = followee_soup.find("h2", class_="zm-list-content-title").a
                            yield user_link["href"]

    def get_followers(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return
        else:
            followers_num = self.followers_num()
            if followers_num == 0:
                return
            else:
                follower_url = self.user_url + "/followers"
                r = requests.get(follower_url)

                soup = BeautifulSoup(r.content)
                for i in xrange((followers_num - 1) / 20 + 1):
                    if i == 0:
                        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
                        for j in xrange(min(followers_num, 20)):
                            print user_url_list[j].a.string.encode("utf-8")
                    else:
                        post_url = "http://www.zhihu.com/node/ProfileFollowersListV2"
                        _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
                        offset = i * 20
                        hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]
                        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
                        data = {
                            '_xsrf': _xsrf,
                            'method': "next",
                            'params': params
                        }
                        header = {
                            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                            'Host': "www.zhihu.com",
                            'Referer': follower_url
                        }
                        r_post = requests.post(post_url, data=data, headers=header)

                        follower_list = r_post.json()["msg"]
                        for j in xrange(min(followers_num - i * 20, 20)):
                            follower_soup = BeautifulSoup(follower_list[j])
                            user_link = follower_soup.find("h2", class_="zm-list-content-title").a
                            print user_link.string.encode("utf-8")


    def get_asks(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return
        else:
            asks_num = self.asks_num()
            if asks_num == 0:
                return
            else:
                for i in xrange((asks_num - 1) / 20 + 1):
                    ask_url = self.user_url + "/asks?page=" + str(i + 1)
                    r = requests.get(ask_url)

                    soup = BeautifulSoup(r.content)
                    for question in soup.find_all("a", class_="question_link"):
                        url = "http://www.zhihu.com" + question["href"]
                        title = question.string.encode("utf-8")
                        yield Question(url, title)

    def get_answers(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return
        else:
            answers_num = self.answers_num()
            if answers_num == 0:
                return
            else:
                for i in xrange((answers_num - 1) / 20 + 1):
                    answer_url = self.user_url + "/answers?page=" + str(i + 1)
                    r = requests.get(answer_url)
                    soup = BeautifulSoup(r.content)
                    for answer in soup.find_all("a", class_="question_link"):
                        yield Answer("http://www.zhihu.com" + answer["href"])




class Question:
    url = None
    soup = None

    def __init__(self, url, title=None):

        if url[0:len(url) - 8] != "http://www.zhihu.com/question/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url

        if title != None: self.title = title

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_title(self):
        if hasattr(self, "title"):
            return self.title
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            title = soup.find("h2", class_="zm-item-title").string.encode("utf-8").replace("\n", "")
            self.title = title
            return title

    def get_detail(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        detail = soup.find("div", id="zh-question-detail").div.get_text().encode("utf-8")
        return detail

    def get_answers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        answers_num = 0
        if soup.find("h3", id="zh-question-answer-num") != None:
            answers_num = int(soup.find("h3", id="zh-question-answer-num")["data-num"])
        return answers_num

    def get_followers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        try:
            followers_num = int(soup.find("div", class_="zg-gray-normal").a.strong.string)
        except AttributeError:
            followers_num = 0
        return followers_num

    def get_topics(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        topic_list = soup.find_all("a", class_="zm-item-tag")
        topics = []
        for i in topic_list:
            topic = i.contents[0].encode("utf-8").replace("\n", "")
            topics.append(topic)
        return topics

class Answer:
    answer_url = None
    # session = None
    soup = None

    def __init__(self, answer_url, question=None, author=None, upvote=None, content=None):
        self.answer_url = answer_url
        if question != None:
            self.question = question
        if author != None:
            self.author = author
        if upvote != None:
            self.upvote = upvote
        if content != None:
            self.content = content

    def parser(self):
        r = requests.get(self.answer_url)
        soup = BeautifulSoup(r.content)
        self.soup = soup

    def get_question(self):
        if hasattr(self, "question"):
            return self.question
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            question_link = soup.find("h2", class_="zm-item-title zm-editable-content").a
            url = "http://www.zhihu.com" + question_link["href"]
            return url

    def get_author(self):
        if hasattr(self, "author"):
            return self.author
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            author_tag = soup.find("div", class_="zm-item-answer-author-info").find_all("a")[1]
            author_url = "http://www.zhihu.com" + author_tag["href"]

            return author_url

    def get_upvote(self):
        if hasattr(self, "upvote"):
            return self.upvote
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            count = soup.find("span", class_="count").string
            if count[-1] == "K":
                upvote = int(count[0:(len(count) - 1)]) * 1000
            elif count[-1] == "W":
                upvote = int(count[0:(len(count) - 1)]) * 10000
            else:
                upvote = int(count)
            return upvote

    def get_content(self):
        if hasattr(self, "content"):
            return self.content
        else:
            if self.soup == None:
                self.parser()
            soup = BeautifulSoup(self.soup.encode("utf-8"))
            try:
                answer = soup.find("div", class_="zm-editable-content clearfix").text.replace("\n","")
                return answer
            except:
                return None