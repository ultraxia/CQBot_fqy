# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import _thread
import time
from modian import newOrder
import copy
from weibo import getidarray, get_5_idarray, checkretweet, checkpic, getscheme, getretweetweibo, getweibo, getpic
from setting import groupid, md_interval, kd_interval, wb_interval
from CQLog import INFO, WARN
# 引入时间调度器 apscheduler 的 BlockingScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


# 与group.py设置一样
bot = CQHttp(api_root='http://127.0.0.1:5700/')
# 实例化 BlockingScheduler
sched = BlockingScheduler()

global weibo_id_array
global firstcheck_weibo

weibo_id_array = []
firstcheck_weibo = True

# 查询时间间隔初始化
interval_md = md_interval()
interval_wb = wb_interval()



def getModian():
    # bot = CQHttp(api_root='http://127.0.0.1:5700/')
    try:
        # INFO(printStrTime() + 'check modian')
        INFO('check modian')
        stampTime = int(time.time())
        msgDict_array = newOrder(stampTime, int(interval_md))
        for msgDict in msgDict_array:
            if msgDict:
                for msg in msgDict['msg']:
                    # msg += msgDict['end']
                    bot.send_group_msg_async(group_id=groupid(), message=msg, auto_escape=False)
                time.sleep(0.1)
    except Exception as e:
        WARN('error when getModian')
    finally:
        # INFO(printStrTime() + 'modian check completed')
        INFO('modian check completed')


def getWeibo():
    # bot = CQHttp(api_root='http://127.0.0.1:5700/')
    try:
        # INFO(printStrTime() + 'check weibo')
        INFO('check weibo')
        global weibo_id_array
        global firstcheck_weibo
        wbcontent = ''
        idcount = -1
        if (firstcheck_weibo == 1):
            # INFO(printStrTime() + 'first check weibo')
            INFO('first check weibo')
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
                    # print(printStrTime() + wbcontent)
                    bot.send_group_msg_async(group_id=groupid(), message=wbcontent, auto_escape=False)
    except Exception as e:
        WARN('error when getWeibo')
    finally:
        # INFO(printStrTime() + 'weibo check completed')
        INFO('weibo check completed')


if interval_md != 0:
    sched.add_job(getModian, 'interval',max_instances=20, seconds=interval_md)
if interval_wb != 0:
    sched.add_job(getWeibo, 'interval',max_instances=20, seconds=interval_wb)
# 开始调度任务
sched.start()
