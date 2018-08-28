#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,logging
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from database import account_data
from lib import logger

# 创建日志对象
atm_log = logger.mylog('atm')

def auth(ids,passwd):
    '''
    验证函数，验证输入的数据是否与数据库内的数据相符
    :param ids: 卡号
    :param passwd: 密码
    :return: 返回该卡号的用户数据
    '''
    data = account_data.load(ids)
    if data:
        if ids == data['id'] and passwd == data['password']:
            return data
def login():
    '''
    登录验证函数
    :return: 返回正确的用户数据
    '''
    ids = input('请插入您的银行卡：').strip()
    passwd = input('请输入您的密码：').strip()
    userdata = auth(ids,passwd)
    while  not  userdata:
        print('验证失败，请重新操作')
        ids = input('请插入您的银行卡：').strip()
        passwd = input('请输入您的密码:').strip()
        userdata = auth(ids,passwd)
    else:
        print('验证成功')
        atm_log.info('account-%s logined'%ids)
        return userdata


