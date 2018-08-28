#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from conf import settings
base_path = settings.base_path
from core import subsystem
from bin import initialize

# 运行主函数
def run():
    initialize.initialize() #初始化系统
    subsystem.run()

if __name__ == '__main__':
    run()