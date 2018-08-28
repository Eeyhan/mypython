#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,socket
# 默认根目录
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from lib import load_dump_data

login_flag = False  # 登录标志位
userdata = []       # 临时存储用户数据

def login(func):
    '''
    登录函数
    :param func: 外部函数
    :return:
    '''
    def inner(arg=None):
        global login_flag
        global userdata
        while not login_flag:
            username = input('uername:').strip()
            password = input('password:').strip()
            data = auth(username,password)
            if data:
                print('登录成功')
                login_flag = True
                userdata = data
                return func(userdata)
            else:
                print('登录失败')
        else:
            return func(userdata)
    return inner

def auth(username,password):
    '''
    验证数据正确性
    :param username: 用户名
    :param password:  密码
    :return:
    '''
    data = {}
    usersdata = load_dump_data.load_data()
    if username in usersdata and password == usersdata[username]['password']:
        data[username] = usersdata[username]
        return data
