#-*- coding:utf-8 -*-

from zhihu_api import User,Answer,Question,page_exist

import db,sys
import threading

reload(sys)
sys.setdefaultencoding('utf8')

users = db.get_existing("users")
pool_questions = db.get_existing("questions")

i = 0
saved_num = 17406

for user in users:
    print i,user
    i += 1
    if i < saved_num:
        continue
    else:
        if User(user).asks_num()!=0:
            j = 0
            try:
                questions = User(user).get_asks()
                for question in questions:
                    if question.url not in pool_questions:
                        if page_exist(question.url):
                            url = question.url
                            tmp = Question(url)
                            try:
                                db.insert_question(tmp.get_title(),url,tmp.get_followers_num(),tmp.get_answers_num(),tmp.get_detail())
                                j += 1
                            except Exception as e:
                                print question.url,e
                        else:
                            print question.url+"404 not found"
                        pool_questions.add(question.url)
            except Exception as e:
                print user,e
            print ("saved %d new questions" % j)
        else:
            print "no questions"