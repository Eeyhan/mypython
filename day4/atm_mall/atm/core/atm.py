#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from lib import main
from lib import login_auth

def run():
    '''
    主函数，登录验证+交易操作
    :return:
    '''
    print('-------------欢迎使用，请插入您的银行卡-------------')
    data = login_auth.login()       # 登录验证并返回数据
    if data:
        main.main(data)             # 调用主模块main下的主函数进行交易操作


