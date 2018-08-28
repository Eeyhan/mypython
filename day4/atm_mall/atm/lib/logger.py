#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import logging,sys,os
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from conf import settings

def mylog(log_type):
    # 创建一个文件型日志对象
    log_file = settings.logging_file[log_type]
    filehand = logging.FileHandler(log_file)
    filehand.setLevel(settings.level)

    # 创建一个输出到屏幕日志对象
    # streamhand = logging.StreamHandler()
    # streamhand.setLevel(settings.level)

    # 设置日志格式
    formater = logging.Formatter(settings.logging_format)

    # 添加格式到文件和输出日志对象中
    filehand.setFormatter(formater)
    # streamhand.setFormatter(formater)

    # 创建log对象，命名
    logger = logging.getLogger(log_type)
    logger.handlers.clear()
    logger.setLevel(settings.level)

    # 把文件型日志和输出型日志对象添加进logger
    logger.addHandler(filehand)
    # logger.addHandler(streamhand)
    return logger


