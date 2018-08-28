#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from conf import settings
from lib import main

# 初始化系统，创建管理员账号
def initialize():
    if not os.listdir(settings.data_path['admin']):
        print('\033[33;1m检测到目前系统暂无账户数据，请先创建一个管理员账号\033[0m')
        main.create_admin()

# 创建账号
def create_account(type):
    if type == 'admin':
        main.create_admin()
    elif type == 'teacher':
        main.create_teacher()
    elif type == 'student':
        main.create_student()