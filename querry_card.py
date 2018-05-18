# Copyright (c) 2018 奥特虾
import pymysql



header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

def connect_database():
    mysql_conn = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'db': '',
            'charset': 'utf8'
        }
    db = pymysql.connect(**mysql_conn)
    cursor = db.cursor()
    return db


def querry(nickname):
    cardList = []
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("select distinct(cardname) from (select * from fqy_card union select * from card_pk1) aa where nickname = %s" , nickname)
    results = cursor.fetchall()
    for row in results:
        row = row[0] + '  '
        cardList.append(row)
    msg = '%s目前已经解锁的卡片有：\n'  % (nickname)
    for card in cardList:
        msg += card
    end = '\n累计解锁%s张，再接再厉！'  % str(len(cardList))
    msg = msg + end
    
    return msg