# Copyright (c) 2018 奥特虾
import pymysql
import card
from cqhttp import CQHttp
bot = CQHttp(api_root='http://127.0.0.1:5700/')

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


def check_data(nickname):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("select count(*) from strawberry where nickname = %s and backer_money >= 10 and pay_time >= '2018-05-15 23:34:14'" , nickname)
    pay_count = cursor.fetchall()[0][0]
    cursor.execute("select count(*) from fqy_card where nickname = %s" , nickname)
    card_count = cursor.fetchall()[0][0]
    diff = int(pay_count) - int(card_count)
    if card_count < pay_count:
        file = card.percent_20()
        cardname = file[6:-4]
        head = '验证通过！ %s 聚聚目前有 %s 张卡未领取，奉上一张补抽卡~' % (nickname,str(diff))
        end = '今后也要继续支持源源哦~'
        msg = [
    {
        'type': 'text',
        'data': {
            'text': head
        }
    },
    {
        'type': 'image',
        'data': {
            'file': file
        }
    },
    {
        'type': 'text',
        'data': {
            'text': end
        }
    },
]
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("INSERT INTO fqy_card VALUES (%s,%s,%s,%s,%s)", (pro_id,nickname,cardname,backer_money,str(pay_time)))
        db.commit()
        db.close()
    
    else:
        msg = '系统检测到你没有需要补抽的卡喔，如有遗漏请联系管理员处理'

    return msg

pro_id = 17044
backer_money = 10
pay_time = '0000-00-00 00:00:00'
