#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from lib import login_auth
from lib import admin_api
from lib import teacher_api
from lib import student_api
from lib import load_data
from bin import initialize
from lib import logginer

def login():
    d = '''
    1.我是管理员
    2.我是讲师
    3.我是学生
    '''
    while True:
        print(d)
        inp = input('请输入您的身份(输入“q”退出)：').strip()
        if inp in ('q','Q','quit'):break
        elif inp == '1':
            inp = 'admin'
            logs = logginer.mylog('admin')
        elif inp == '2':
            inp = 'teacher'
            logs = logginer.mylog('teacher')
        elif inp == '3':
            inp = 'student'
            logs = logginer.mylog('student')
        data = load_data.load_data(inp)         # 加载对应身份的数据
        if not data and not inp.isdigit():      # 当没有数据且inp还是数字时
            print('\033[32;1m您还未创建账号，请先创建账号再登录账号\033[0m')
            initialize.create_account(inp)
        elif data:
            flag = input('已有账号？[yes/no]').strip()
            if flag in ('y','Y','yes','YES'):
                print('\033[32;1m请登录账号\033[0m')
                userdata = login_auth.login(inp)
                if userdata.level == '0':
                    logs.info('%s login successful'%userdata.admin_name)
                elif userdata.level == '1':
                    logs.info('%s login successful'%userdata.teacher_name)
                else:
                    logs.info('%s login successful'%userdata.student_name)
                return userdata
            else:
                print('\033[32;1m请注册账号\033[0m')
                initialize.create_account(inp)
        else:
            print('\033[31;1m输入有误\033[0m')

def ctrl(data):
    if data.level == '0':
        # 管理员视图接口
        admin_api.admin(data)
    elif data.level == '1':
        # 讲师视图接口
        teacher_api.teacher(data)
    elif data.level == '2':
        # 学生视图接口
        student_api.student(data)

def run():
    userdata = login()
    if userdata:    # 如果有数据
        print('\033[32;1m登录成功，进入选课系统\033[0m')
        ctrl(userdata)
if __name__ == '__main__':
    run()