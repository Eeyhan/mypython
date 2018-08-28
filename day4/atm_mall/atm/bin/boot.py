#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys

base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from core import atm

def main():
    '''
    接口函数，调用主程序模块atm下的主函数run
    :return:
    '''
    atm.run()
if __name__ == '__main__':
    main()