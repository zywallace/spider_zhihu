#-*- coding:utf-8 -*-

from zhihu_api import User,Answer,Question,page_exist

import db,sys

reload(sys)
sys.setdefaultencoding('utf8')

users = db.get_existing("users")
pool_answers = db.get_existing("answers")
i = 1
saved_num = 1277

for user in users:
    print i,user
    i += 1
    if i < saved_num :
        continue
    else:
        if User(user).answers_num()!=0:
            j = 0
            answers = User(user).get_answers()
            for answer in answers:
                if answer.answer_url not in pool_answers:
                    if page_exist(answer.answer_url):
                        url = answer.answer_url
                        tmp = Answer(url)
                        if tmp.get_content()!= None:
                            try:
                                db.insert_answer(tmp.answer_url,tmp.get_author(),tmp.get_content(),tmp.get_upvote(),tmp.get_question())
                                j += 1
                            except Exception as e:
                                print  answer.answer_url,e
                        else:
                            print answer.answer_url+"被折叠"
                    else:
                        print answer.answer_url+"404 not found"
                    pool_answers.add(answer.answer_url)
            print ("saved %d new answers" % j)

        else:
            print "no ansewer"