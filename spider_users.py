#-*- coding:utf-8 -*-

from zhihu_api import User
import Queue,db,sys


reload(sys)
sys.setdefaultencoding('utf8')

initial_page = u'http://www.zhihu.com/people/liu-yang-57-86'
url_queue = Queue.Queue()
seen = db.get_existing("users")
seen.add(initial_page)
url_queue.put(initial_page)
while(True): #一直进行直到海枯石烂
    if url_queue.qsize()>0:
        current_url = url_queue.get()    #拿出队例中第一个的url
        #store(current_url)               把这个url代表的网页存储好
        for next_url in User(current_url).get_followees(): #提取把这个url里链向的url
            if next_url not in seen:
                seen.add(next_url)
                try:
                    name,url,followees_num,followers_num,thanks_num,agree_num,asks_num,answers_num = User(next_url).get_info()
                    db.insert_user(name,url,followees_num,followers_num,thanks_num,agree_num,asks_num,answers_num)
                except:
                    print next_url+'用户不存在'
                url_queue.put(next_url)
    else:
        break