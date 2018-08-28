#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from conf import settings
from lib import load_data

def login(identity):
    while True:
        username = input('用户名: ').strip()
        password = input('密码: ').strip()
        userdata = auth(identity,username,password)
        if userdata:
            return userdata
        else:
            print('\033[31;1m登录失败，请重新登录\033[0m')

def auth(identity,username,password):
    data = load_data.load_data(identity)
    if identity == 'admin':
        for i in data:
            if username == i.admin_name and password == i.password:
                return i
    elif identity == 'student':
        for i in data:
            if username == i.student_name and password == i.password:
                return i
    elif identity == 'teacher':
        for i in data:
            if username == i.teacher_name and password == i.password:
                return i
