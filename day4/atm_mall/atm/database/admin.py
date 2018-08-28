#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
import os,random,json,shutil

# 当前文件的根目录
path = os.path.dirname(__file__)

def check_account():
    '''
    查看所有账户卡号
    :return:
    '''
    allfile = os.listdir(path)
    print('------ 用户id -----')
    for i in allfile:
        if i.startswith('6'):
            print(i)
    print('-------------------')

def add_account():
    '''
    添加账户
    :return:
    '''
    name = input('username:').strip()
    ids =  66662200+random.randint(2,100)
    password = input('password:').strip()
    balance = input('balance:').strip()
    if not name or not password or not balance: #默认账户数据模板
        name = 'lucy'
        password = '666666'
        balance = 15000
    data = {}
    data['name'] = name                 # 姓名
    data['id'] = str(ids)               # 卡号
    data['password'] = password         # 密码
    data['balance'] = float(balance)    # 额度
    data['status'] = 0                  # 账户状态，正常为0，异常为1
    data['bill'] = {"trans": [], "shop": [], "draw": []}    # 账单，默认全为空
    data['cart'] = []                   # 购物车
    data['arrears'] = 0                 # 余额，默认为0，正数为余额，负数为欠款
    filepath= os.path.join(path,str(ids))
    while  os.path.exists(filepath):
        ids =  66662200+random.randint(1,100)
        filepath= os.path.join(path,str(ids))
    f = open(filepath,'w')
    json.dump(data,f)
    print('已添加账户 %s'%data['id'])

def delete_account():
    '''
    删除账户
    :return:
    '''
    check_account()
    ids = input('请输入待删除的账户id: ')
    deleted_ducoment = os.path.join(path,'deleted')
    filename = str(ids)
    if not os.path.exists(deleted_ducoment):
        os.makedirs(deleted_ducoment)
    os.rename(filename,'del.'+filename)
    shutil.move('del.'+filename,deleted_ducoment)
    print('已删除账户 %s'%ids)

def frozen_account():
    '''
    冻结账户
    :return:
    '''
    check_account()
    ids = input('请输入待冻结的账户id: ')
    filepath = os.path.join(path,ids)
    if os.path.exists(filepath):
        f = open(filepath,'r')
        data = json.load(f)
        if data['status'] == 0:
            data['status'] = 1
            f = open(filepath,'w')
            json.dump(data,f)
            print('已冻结账户 %s'%ids)
        else:
            print('账户 %s 已被冻结，无需冻结'%ids)

def unfrozen_account():
    '''
    解冻用户
    :return:
    '''
    check_account()
    ids = input('请输入待解冻的账户id: ')
    filepath = os.path.join(path,ids)
    if os.path.exists(filepath):
        f = open(filepath,'r')
        data = json.load(f)
        if data['status'] == 1:
            data['status'] = 0
            f = open(filepath,'w')
            json.dump(data,f)
            print('已解冻账户 %s'%ids)
        else:
            print('账户 %s 未被冻结，无需解冻'%ids)

def update_balance():
    '''
    解冻用户
    :return:
    '''
    check_account()
    ids = input('请输入待待调整的账户id: ')
    filepath = os.path.join(path,ids)
    if os.path.exists(filepath):
        f = open(filepath,'r')
        data = json.load(f)
        chos = input('该账户额度为 %.2f \n是否需要调整？yes/no: '%data['balance']).strip()
        if chos in ('yes','Yes','y','Y'):
            cash = input('请输入新的额度：').strip()
            while not  cash.isdigit():
                cash = input('额度必须为数字，请重新输入：').strip()
            else:
                print('该账户已调整额度为%s'%cash)
                data['balance'] = float(cash)
        else:
            print('操作取消')
        f = open(filepath,'w')
        json.dump(data,f)


options = {
    '1':check_account,
    '2':add_account,
    '3':delete_account,
    '4':frozen_account,
    '5':unfrozen_account,
    '6':update_balance
}

flag = False
while True:
    print('''
    1.查看账户
    2.添加账户
    3.删除账户
    4.冻结账户
    5.解冻账户
    6.调整额度
    ''')
    chos = input('(“q” 退出)>>> ')
    if chos in ('q','Q','quit'):
        break
    if chos not in options:
        print('错误，请重新输入')
    else:
        options[chos]()
print('-------bye--------')