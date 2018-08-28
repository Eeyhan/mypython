#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,logging

# 默认文件路径
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

# 日志级别
level = logging.INFO

# 日志文件分类处理
logging_file ={
    'atm':os.path.join(base_path,'log','atm_log.log'),
    'mall':os.path.join(base_path,'log','mall_log.log')
}

# 日志格式
logging_format = '%(asctime)s -- %(levelname)s -- %(filename)s -- %(message)s '

