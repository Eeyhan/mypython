#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from lib.transaction import check
from lib.transaction import draw
from lib.transaction import repay
from lib.transaction import transfer
from lib.transaction import out

def main(userdata):
    '''
    主函数
    :param userdata: 用户数据
    :return:
    '''
    print('--------XX银行欢迎您---------')
    options = {
        '1':check,
        '2':draw,
        '3':repay,
        '4':transfer,
        '5':out
    }

    while True:
        print('''
        1.查看
        2.取款
        3.还款
        4.转账
        5.退卡'''
        )
        chos = input('>>>: ')
        if chos in options:
            userdata = options[chos](userdata)  # 根据用户的输入调用对应的函数
        else:
            print('操作错误，请重新输入')


