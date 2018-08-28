#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import json,os

# 当前模块的根目录
path = os.path.dirname(__file__)

def load_all():
    '''
    加载当前根目录的所有用户数据
    :return: 返回所有用户数据
    '''
    dataobj = {}
    datalist = os.listdir(path)
    for i in datalist:
        if i.startswith('66662'):
            f = open(os.path.join(path,i),'r',encoding='utf-8')
            dataobj[i] = json.load(f)
            f.close()
    return dataobj

def dump(data):
    '''
    存入用户数据
    :param data: 用户数据
    :return:
    '''
    filename = data['id']
    file = os.path.join(path,filename)
    if os.path.exists(file) and os.path.isfile(file):
        f = open(file,'w',encoding='utf-8')
        json.dump(data,f)
        f.close()
    else:
        print('不存在此账号')

def load(ids):
    '''
    加载对应卡号的用户数据
    :param ids: 卡号
    :return: 返回对应卡号的用户数据
    '''
    if ids in os.listdir(path):
        f = open(os.path.join(path,ids),'r',encoding='utf-8')
        data = json.load(f)
        f.close()
        return data
    else:
        print('不存在的账户')






