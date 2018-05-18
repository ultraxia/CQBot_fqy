# -*- coding: utf-8 -*-
import setting
import requests
import json
import urllib
import hashlib
import time
import pymysql
import card

# -------------------------------
# init
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

def connect_database():
    mysql_conn = {
            'host': '120.25.213.2',
            'port': 3306,
            'user': 'root',
            'password': 'fcc21042',
            'db': 'SNH48',
            'charset': 'utf8'
        }
    db = pymysql.connect(**mysql_conn)
    cursor = db.cursor()
    return db

# 计算签名
def getSign(ret):
    # 将字典按键升序排列，返回一个元组tuple
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    # md5计算 & 十六进制转化 & 根据规则从第6位开始取16位
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign

def getOrders(pro_id, page):
    url = 'https://wds.modian.com/api/project/orders'
    form = {
        'page': page,
        'pro_id': pro_id
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response

def getRankings(pro_id, type, page):
    url = 'https://wds.modian.com/api/project/rankings'
    form = {
        'page': page,
        'pro_id': pro_id,
        'type': type
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response

def getDetail(*pro_id):
    # 将形参（一个元组）中int元素转为str元素，用逗号拼接成字符串
    pro_id_str = ','.join(map(str, pro_id))
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_id_str
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response

def md_init(proid_array):
    array = []
    for id in proid_array:
        dict = {}
        dict['pro_id'] = int(id)
        id_url = 'https://zhongchou.modian.com/item/%d' % int(id)
        try:
            dict['url_short'] = setting.get_short_url(id_url)
        except Exception as e:
            dict['url_short'] = 'https://zhongchou.modian.com/item/%d' % int(id)
        dict['url_long'] = 'https://zhongchou.modian.com/item/%d' % int(id)
        detail = getDetail(id)
        dict['name'] = detail['data'][0]['pro_name']
        array.append(dict)
    return array

# rank
def rank(type):
    msg_array = []
    err = False
    err_msg = '返回rank错误\n'
    pro_id_array = md_init(setting.pro_id())
    for pro_id_dict in pro_id_array:
        msg = ''
        detail = getDetail(pro_id_dict['pro_id'])
        # type=1:总额榜
        if type == 1:
            msg = msg + pro_id_dict['name'] + '·聚聚榜TOP20\n' + '------------\n'
            dic = getRankings(pro_id_dict['pro_id'], 1, 1)
            if int(dic['status']) == 0:
                for data in dic['data']:
                    msg = msg + '【第' + str(data['rank']) + '名】: ' +data['nickname'] + '支持了' + str(data['backer_money']) + '元\n'
            elif int(dic['status']) == 2:
                err = True
                err_msg += dic['message']
        elif type == 2:
            msg = msg + pro_id_dict['name'] + '·打卡榜TOP20\n' + '------------\n'
            dic = getRankings(pro_id_dict['pro_id'], 2, 1)
            if int(dic['status']) == 0:
                for data in dic['data']:
                    msg = msg + '【第' + str(data['rank']) + '名】: ' +data['nickname'] + '已打卡' + str(data['support_days']) + '天\n'
            elif int(dic['status']) == 2:
                err = True
                err_msg += dic['message']
        msg = msg + '------------\n【摩点】：' + 'https://mourl.cc/nHm1a9' + '\n目前集资进度：¥' +\
            str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
            detail['data'][0]['goal']
        msg_array.append(msg)
    if err is True:
        return err_msg
    elif err is False:
        return msg_array


def result(pro_id_array):
    msg_array = []
    for pro_id in pro_id_array:
        response = getDetail(pro_id)
        msg = ''
        msg += response['data'][0]['pro_name'] + '\n' + '项目进度：' + str(response['data'][0]['already_raised']) + '/' + response['data'][0]['goal'] + '\n结束时间：' + response['data'][0]['end_time']
        msg_array.append(msg)
    return msg_array


def newOrder(stamp10, secondsDelay):
    msgDict_array = []
    pro_id_array = md_init(setting.pro_id())
    for pro_id_dict in pro_id_array:
        newOrders = []
        # 获取一次订单信息，返回一个dictionary
        orderDict = getOrders(pro_id_dict['pro_id'], 1)
        # 查询失败则返回错误信息
        if int(orderDict['status']) == 2:
            return orderDict['message']
        # 查询成功，遍历data
        for data in orderDict['data']:
            pay_time = data['pay_time']
            # 将字符串时间转换为unix时间戳
            data['pay_time'] = int(time.mktime(time.strptime(pay_time, '%Y-%m-%d %H:%M:%S')))
            # 筛选订单时间在查询时间前的设定时间段之间的订单
            if data['pay_time'] >= stamp10 - secondsDelay and data['pay_time'] < stamp10:
                newOrders.append(data)
        msgDict = {}
        if newOrders:
            detail = getDetail(pro_id_dict['pro_id'])
            if int(detail['status']) == 2:
                return detail['message']
            msgDict['msg'] = []
            msg = ''
            for newOrder in newOrders:
                pay_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(newOrder['pay_time']))
                if float(newOrder['backer_money']) < 10:
                    msg = "感谢 " + newOrder['nickname'] +\
                        " 聚聚在【" + pro_id_dict['name'] + "】中支持了 ¥" +\
                        str(newOrder['backer_money']) + '集资满10元可以抽卡哦'
                else:
	                if float(newOrder['backer_money']) < 100:
	                    file = card.percent_1()
	                if 100 <= float(newOrder['backer_money']) < 1000:
	                    file = card.percent_20()
	                if float(newOrder['backer_money']) >= 1000:
	                    file = card.percent_100()
	                cardname = file[6:-4]
	                msg = "感谢 " + newOrder['nickname'] +\
	                    " 聚聚在【" + pro_id_dict['name'] + "】中支持了 ¥" +\
	                    str(newOrder['backer_money']) + '\n'+'恭喜获得卡片： ' + cardname
	                end = '【摩点】：' + pro_id_dict['url_short'] + '\n目前集资进度：¥' +\
                str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
                str(detail['data'][0]['goal'])
	                msg = [
	    {
	        'type': 'text',
	        'data': {
	            'text': msg
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
	                cursor.execute("INSERT INTO fqy_card VALUES (%s,%s,%s,%s,%s)", (pro_id_dict['pro_id'],newOrder['nickname'],cardname,newOrder['backer_money'],str(pay_time)))
	                db.commit()
	                db.close()   
                msgDict['msg'].append(msg)
            # msgDict['end'] = '【摩点】：' + pro_id_dict['url_short'] + '\n目前集资进度：¥' +\
                # str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
                # str(detail['data'][0]['goal'])
            msgDict_array.append(msgDict)
    return msgDict_array
