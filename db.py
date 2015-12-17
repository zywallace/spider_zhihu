#-*- coding:utf-8 -*-

import MySQLdb,sys

reload(sys)
sys.setdefaultencoding('utf8')


def get_existing(db):
    con = MySQLdb.connect(host="localhost", user="root", passwd="19930611a",db="python_test",port=3306,charset='utf8')
    cur = con.cursor()
    sql ="select url from "+db
    cur.execute(sql)
    tmp = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return tuple2set(tmp)

def insert_question(title,url,followers_num, answers_num,content):
    con = MySQLdb.connect(host="localhost", user="root", passwd="19930611a",db="python_test",port=3306,charset='utf8')
    cur = con.cursor()
    cur.execute("insert into questions (title,url,followers_num,answers_num,content) values (%s,%s,%s,%s,%s)", \
                (title,url,followers_num,answers_num,content))
    con.commit()
    cur.close()
    con.close()

def tuple2set(tuple_list):
    tmp = set()
    for tuple in tuple_list:
        tmp2=tuple[0].decode("utf-8")
        tmp.add(tmp2)
    return tmp

def insert_user(name,url,followees_num,followers_num,thanks_num,agree_num,asks_num, answers_num):
    con = MySQLdb.connect(host="localhost", user="root", passwd="19930611a",db="python_test",port=3306,charset='utf8')
    cur = con.cursor()
    cur.execute("insert into users (name,url,followees_num,followers_num,thanks_num,agree_num,asks_num,answers_num) values (%s,%s,%s,%s,%s,%s,%s,%s)", \
                (name,url,followees_num,followers_num,thanks_num,agree_num,asks_num,answers_num))

    con.commit()
    cur.close()
    con.close()

def insert_answer(url,author_url,content,upvote,question_url):
    con = MySQLdb.connect(host="localhost", user="root", passwd="19930611a",db="python_test",port=3306,charset='utf8')
    cur = con.cursor()
    cur.execute("insert into answers (url,author_url,content,upvote,question_url) values (%s,%s,%s,%s,%s)", \
                (url,author_url,content,upvote,question_url))
    con.commit()
    cur.close()
    con.close()