#-*- coding:utf-8 -*-

from zhihu_api import User,Answer,Question

import Queue,db,sys

reload(sys)
sys.setdefaultencoding('utf8')


users = db.get_existing("users")
pool = db.get_existing("questions")

for user in users:
    questions = User(user).get_asks()
    answers = User(user).get_answers()
    if questions != None:
        for question in questions:
            if question.url not in pool:
                url = question.url
                tmp = Question(url)
                db.insert_question(tmp.get_title(),url,tmp.get_followers_num(),tmp.get_answers_num(),tmp.get_detail())