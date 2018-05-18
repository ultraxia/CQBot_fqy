# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import setting
import modian
import pk_broad
import peopleNum
import querry_card
import add_card
import admin
import add_card_auto
import fans_db
import querry_price
import random

bot = CQHttp(api_root='http://127.0.0.1:5700/')


# 群消息操作
@bot.on_message()
def handle_msg(context):
    if  context['user_id'] != context['self_id']:
        if setting.shutup():
            for word in setting.shutup():
                if word in context['message']:
                    bot.set_group_ban(group_id=setting.groupid(), user_id=context['user_id'], duration=30*60)

        if context['message'] == 'wds20' or context['message'] == 'jz20' or context['message'] == 'rank':
            rank1_array = modian.rank(1)
            for rank1_msg in rank1_array:
                bot.send(context, rank1_msg)
        elif context['message'] == 'dkb' or context['message'] == '打卡榜' :
            rank2_array = modian.rank(2)
            for rank2_msg in rank2_array:
                bot.send(context, rank2_msg)
        elif context['message'] == '项目进度' or context['message'] == '进度':
            jd_array = modian.result(setting.pro_id())
            jd = ''
            for jd_msg in jd_array:
                jd += jd_msg 
            bot.send(context, jd)
        elif '我的卡片：' or '我的卡片:' in context['message']:
            nickname = context['message'][5:]
            mycard = querry_card.querry(nickname)
            bot.send(context,mycard)
        elif context['message'][:3] == '补卡:' or context['message'][:3] == '补卡：' :
            nickname = context['message'][3:]
            buka = add_card_auto.check_data(nickname)
            bot.send(context,buka)



# 新人加群提醒
@bot.on_event('group_increase')
def handle_group_increase(context):
    if context['group_id'] == setting.groupid():
        welcome = [{'type': 'text', 'data': {'text': '欢迎新聚聚：'}},
        {'type': 'at', 'data': {'qq': str(context['user_id'])}},
        {'type': 'text', 'data': {'text': '，进了应援会的门就是源源的人\n%s' % setting.welcome()}}
        ]
        bot.send(context, message=welcome, is_raw=True)  # 发送欢迎新人


# 如果修改了端口，请修改http-API插件的配置文件中对应的post_url
bot.run(host='127.0.0.1', port=8080)
