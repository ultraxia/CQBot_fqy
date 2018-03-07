mport setting
import requests
import json
import urllib
import hashlib
import time

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

pro_id = 11696

# 计算签名
def getSign(ret):
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
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
    while True:
        form = {
            'page': page,
            'pro_id': pro_id,
            'type': type
        }
        sign = getSign(form)
        form['sign'] = sign
        response = requests.post(url, form, headers=header).json()
        page += 1
        if datas == []:
            break
        for data in datas:
            userid.append(data['nickname'])
            price.append(data['backer_money'])
        return response

def getDetail(*pro_id):
    pro_id_str = ','.join(map(str, pro_id))
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_id_str
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response

# rank
def rank(type):
    msg = ''
    err = False
    err_msg = '返回rank错误\n'
    detail = getDetail(str(setting.pro_id()))
    if type == 1:
        msg = msg + setting.wds_name() + '·聚聚榜TOP20\n' + '------------\n'
        dic = getRankings(setting.pro_id(), 1, 1)
        if int(dic['status']) == 0:
            for data in dic['data']:
                msg = msg + '【第' + str(data['rank']) + '名】: ' +data['nickname'] + '支持了' + str(data['backer_money']) + '元\n'
        elif int(dic['status']) == 2:
            err = True
            err_msg += dic['message']
    elif type == 2:
        msg = msg + setting.wds_name() + '·打卡榜TOP20\n' + '------------\n'
        dic = getRankings(setting.pro_id(), 2, 1)
        if int(dic['status']) == 0:
            for data in dic['data']:
                msg = msg + '【第' + str(data['rank']) + '名】: ' +data['nickname'] + '已打卡' + str(data['support_days']) + '天\n'
        elif int(dic['status']) == 2:
            err = True
            err_msg += dic['message']
    msg = msg + '【摩点】：' + setting.wds_url() + '\n目前集资进度：¥' +\
        str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
        detail['data'][0]['goal']
    if err is True:
        return err_msg
    elif err is False:
        return msg


def newOrder(stamp10, secondsDelay):
    newOrders = []
    orderDict = getOrders(setting.pro_id(), 1)
    if int(orderDict['status']) == 2:
        return orderDict['message']
    for data in orderDict['data']:
        pay_time = data['pay_time']
        data['pay_time'] = int(time.mktime(time.strptime(pay_time, '%Y-%m-%d %H:%M:%S')))
        if data['pay_time'] >= stamp10 - secondsDelay and data['pay_time'] < stamp10:
            newOrders.append(data)
    msgDict = {}
    if newOrders:
        detail = getDetail(setting.pro_id())
        if int(detail['status']) == 2:
            return detail['message']
        msgDict['msg'] = []
        msg = ''
        for newOrder in newOrders:
            nickname = newOrder['nickname']
            rank = str(searchRank(nickname))
            if rank != '1':
                msg = "感谢 " + newOrder['nickname'] +\
                    " 聚聚在【" + setting.wds_name() + "】中支持了 " +\
                    str(newOrder['backer_money']) + "元,当前排行榜第" + rank +"名,距离上一名相差"+\
                    str(computeDiff(nickname)) + '元\n'
            else:
                msg = "感谢 " + newOrder['nickname'] +\
                    " 爸爸在【" + setting.wds_name() + "】中支持了 " +\
                    str(newOrder['backer_money']) + "元,当前排行榜第" + rank +"名！！源源爱你哟！\n"

            msgDict['msg'].append(msg)
        msgDict['end'] = '【摩点】：' + setting.wds_url() + '\n目前集资进度：¥' +\
            str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
            str(detail['data'][0]['goal'])
    return msgDict

def getRank():
    dataDict = []
    page = 1
    url = 'https://wds.modian.com/api/project/rankings'
    while True:
        form = {
            'page': page,
            'pro_id': pro_id,
            'type': 1
        }
        sign = getSign(form)
        form['sign'] = sign
        response = requests.post(url, form, headers=header).json()
        page += 1
        datas = response['data']
        if datas == []:
            break   
        for data in datas:
            dataDict.append(data)    
    return dataDict

def searchRank(nickname):
    dataDict = getRank()
    for data in dataDict:
        if data['nickname'] == nickname:
            rank = data['rank']
            return rank

def computeDiff(nickname):
    dataDict = getRank()
    rank = searchRank(nickname) - 1
    lastrank = rank - 1
    backer_money = dataDict[rank]['backer_money']
    last_backer_money = dataDict[lastrank]['backer_money']
    diff = float(last_backer_money) - float(backer_money)
    diff = '%.2f' % diff
    return diff
    
