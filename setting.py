# -*- coding: utf-8 -*-
import random
import configparser
import os
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 小偶像名字
def idol_name():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # idol name
        idol_name = cf.get('idol', 'name')
    return str(idol_name)


# ----------------------摩点微打赏设置----------------------


# 微打赏名称
def wds_name():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        modian_name = cf.get('modian', 'name')
        # modian_url = cf.get('modian', 'url')
        # pro_id = cf.get('modian', 'pro_id')
    return str(modian_name)


# 微打赏网址 建议使用短地址t.cn
def wds_url():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        # modian_name = cf.get('modian', 'name')
        modian_url = cf.get('modian', 'url')
        # pro_id = cf.get('modian', 'pro_id')
    return str(modian_url)


# 微打赏项目对应pro_id
def pro_id():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        # modian_name = cf.get('modian', 'name')
        # modian_url = cf.get('modian', 'url')
        pro_id = cf.get('modian', 'pro_id')
    return int(pro_id)



# --------------------------------------------------------



# ----------------------qq群设置----------------------


# qq群id
def groupid():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        group_id = cf.get('QQqun', 'id')
    return int(group_id)


# 欢迎信息
def welcome():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # group_welcome
        words = cf.get('QQqun', 'welcome')
        msg = words.replace('\\n', '\n')
    return msg


# 关键词触发
# 禁言关键词,留空则无禁言
def shutup():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        shutword = cf.get('QQqun', 'shutword')
        if shutword:
            wordlist = shutword.split(',')
        else:
            wordlist = []
    return wordlist


# --------------------------------------------------------


# ----------------------微博设置----------------------


# 手机网页版微博地址
def weibo_url():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        weibo_url = cf.get('weibo', 'weiboURL')
    return str(weibo_url)


# weibo container id
def weibo_id():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        weibo_id = cf.get('weibo', 'weiboID')
    return int(weibo_id)


# --------------------------------------------------------


# ----------------------代理设置----------------------


def proxy():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        https = cf.get('proxy', 'https')
        if https:
            list_https = https.split(',')
            proxies = {}
            proxies['https'] = random.choice(list_https)
        else:
            list_https = []
            proxies = {}
    # list_http = ['113.118.98.220:9797', '183.62.196.10:3128', '61.135.217.7:80', '61.155.164.109:3128', '61.155.164.107:3128']
    # list_https = ['114.115.140.25:3128', '59.56.74.205:3128', '116.31.75.97:3128', '121.43.178.58:3128', '113.79.75.82:9797']
    # proxies['http'] = random.choice(list_http)
    # proxies['https'] = random.choice(list_https)
    return proxies


# --------------------------------------------------------
