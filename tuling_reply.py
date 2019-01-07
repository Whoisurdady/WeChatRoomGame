#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
import itchat, time
from itchat.content import *

import game_chengyu
import json



import requests
import itchat

KEY = '******' # regitster your own KEY here, web site http://www.tuling123.com/member/robot/index.jhtml

game_dict = {}

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def tuling_reply_group_at(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    # print(msg)
    defaultReply = 'I received: ' + msg['Text']
    print(msg.user)
    if msg.isAt:

        # 如果图灵Key出现问题，那么reply将会是None
        reply = get_response(msg['Text'])
        print(reply or defaultReply)
        msg.user.send(u'@%s %s' % (
            msg.actualNickName, reply or defaultReply))

    game_reply = game_chengyu.game_run(msg['Text'].decode("utf-8"), msg.actualNickName or get_friend_name(msg))
    if game_reply:
        msg.user.send(game_reply)

    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
#     return reply or defaultReply

def get_friend_name(msg):
    from_uid = msg["FromUserName"]
    return itchat.search_friends(userName=from_uid)['NickName'].decode('utf-8')


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply_chat(msg):
    # msg_dict = json.load(msg)
    # print(msg.userInfo)
    game_reply = game_chengyu.game_run(msg['Text'].decode("utf-8"), get_friend_name(msg))
    if game_reply:
        return game_reply
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    # print(msg)
    defaultReply = 'I received: ' + msg['Text']
    reply = u'[赵二狗]%s' % (get_response(msg['Text']))
    
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    print(reply or defaultReply)
    return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
game_chengyu.init()
itchat.auto_login(hotReload=True)
itchat.run()
