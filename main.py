# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import _thread
import time
from modian import newOrder
import copy
from weibo import getidarray, get_5_idarray, checkretweet, checkpic, getscheme, getretweetweibo, getweibo, getpic
from setting import groupid
from CQLog import INFO, WARN


global weibo_id_array
global firstcheck_weibo

weibo_id_array = []
firstcheck_weibo = True


def printStrTime():
    t = int(time.time()*1000)
    x = time.localtime(t / 1000)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return time_str


def getModian(delay):
    bot = CQHttp(api_root='http://127.0.0.1:5700/')
    while True:
        stampTime = int(time.time())
        msgDict = newOrder(stampTime, int(delay))
        if msgDict:
            for msg in msgDict['msg']:
                msg += msgDict['end']
                bot.send_group_msg_async(group_id=groupid(), message=msg, auto_escape=False)
                time.sleep(0.1)
        time.sleep(int(delay))


def getWeibo(delay):
    bot = CQHttp(api_root='http://127.0.0.1:5700/')
    while True:
        global weibo_id_array
        global firstcheck_weibo
        wbcontent = ''
        idcount = -1
        if (firstcheck_weibo == 1):
            weibo_id_array = copy.copy(getidarray())
            firstcheck_weibo = False
        checkwbid = copy.copy(get_5_idarray())
        if (firstcheck_weibo == 0):
            for cardid in checkwbid:
                idcount += 1
                if int(cardid) == 0:
                    continue
                if cardid not in weibo_id_array:
                    weibo_id_array.append(cardid)
                    retweet = checkretweet(idcount)
                    wbpic = checkpic(idcount)
                    wbscheme = getscheme(idcount)
                    if (retweet):
                        wbcontent = "源源刚刚[转发]了一条微博：" + '\n' + '\n' + getretweetweibo(idcount) + '\n'
                        wbcontent = wbcontent + '\n' + "传送门：" + wbscheme
                    else:
                        wbcontent = "源源刚刚发了一条新微博：" + '\n' + '\n' + getweibo(idcount) + '\n'
                        if (wbpic):
                            wbcontent = wbcontent + getpic(idcount)
                        wbcontent = wbcontent + '\n' + "传送门：" + wbscheme
                    bot.send_group_msg_async(group_id=groupid(), message=wbcontent, auto_escape=False)
        time.sleep(int(delay))



try:
    _thread.start_new_thread(getModian, (30,))
    _thread.start_new_thread(getWeibo, (60,))
except Exception as e:
    print(printStrTime() + 'Error:  unable to start thread')

while True:
    pass
