# spider_zhihu

使用python爬下来数据，登录的类和爬虫方法使用了https://github.com/egrcc/zhihu-python
爬虫的逻辑为：
1）从初始用户开始，找到他的“关注的人”，作为第二层。采用广度优先算法，采集用户的数据，这样得到的用户起码不是“0粉丝”的用户
这样排除了一些僵尸用户。
伪代码：
    initial_page
    url_queue = Queue.Queue()
    seen.add(initial_page)
    url_queue.put(initial_page)
    while(True): #一直进行直到海枯石烂
        if url_queue.qsize()>0:
            current_url = url_queue.get()    #拿出队例中第一个的url
            #store(current_url)               把这个url代表的网页存储好
            for next_url in User(current_url).get_followees(): #提取把这个url里链向的url
                if next_url not in seen:
                    seen.add(next_url)
                    url_queue.put(next_url)
        else:
            break
2）对于以采集到的用户找到他提的问题，进行数据采集
3）对于以采集到的用户找到他回答的答案，进行数据采集


Table users
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| name          | varchar(50)  | NO   |     | NULL    |       |
| url           | varchar(100) | NO   | PRI | NULL    |       |
| followees_num | int(11)      | NO   |     | NULL    |       |
| followers_num | int(11)      | NO   |     | NULL    |       |
| thanks_num    | int(11)      | NO   |     | NULL    |       |
| agree_num     | int(11)      | NO   |     | NULL    |       |
| asks_num      | int(11)      | NO   |     | NULL    |       |
| answers_num   | int(11)      | NO   |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+
共爬下来22532个users的信息

Table questions
+---------------+-------------+------+-----+---------+-------+
| Field         | Type        | Null | Key | Default | Extra |
+---------------+-------------+------+-----+---------+-------+
| title         | longtext    | NO   |     | NULL    |       |
| answers_num   | int(11)     | NO   |     | 0       |       |
| followers_num | int(11)     | NO   |     | 0       |       |
| content       | longtext    | YES  |     | NULL    |       |
| url           | varchar(50) | NO   | PRI | NULL    |       |
+---------------+-------------+------+-----+---------+-------+
共爬下来152971个问题

Table answers
+--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| url          | varchar(100) | NO   | PRI | NULL    |       |
| author_url   | varchar(100) | NO   |     | NULL    |       |
| content      | longtext     | NO   |     | NULL    |       |
| upvote       | int(11)      | NO   |     | 0       |       |
| question_url | varchar(100) | NO   |     | NULL    |       |
+--------------+--------------+------+-----+---------+-------+
共爬下来1375个用户，关于131823个问题的165498个答案

数据和知乎官方说的上千万个用户以及知乎一些用户估计70-80w左右的活跃用户还是有较大的差距。可能需要修改代码使用多线程进行数据采集。
对于匿名用户进行忽略
