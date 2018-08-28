#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,logging

# base_path
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

# db_path
db_path = os.path.join(base_path,'database')


# 数据文件路径
data_path = {
    'school':os.path.join(db_path,'school'),
    'teacher':os.path.join(db_path,'teacher'),
    'classes':os.path.join(db_path,'classes'),
    'course':os.path.join(db_path,'course'),
    'student':os.path.join(db_path,'student'),
    'admin':os.path.join(db_path,'admin'),
}

# 日志设置

# 日志等级
log_level = logging.INFO

# 日志格式
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 日志文件
logging_file = {
    'admin':os.path.join(base_path,'log','admin.log'),
    'teacher':os.path.join(base_path,'log','teacher.log'),
    'student':os.path.join(base_path,'log','student.log'),
}