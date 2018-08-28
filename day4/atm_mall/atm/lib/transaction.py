#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,datetime,logging
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from database import account_data
from lib import logger

# 创建日志对象
atm_log = logger.mylog('atm')

def check(data):
    '''
    查看账单，可用额度
    :param data: 返回用户数据
    :return:
    '''
    # arrears = sum(list(data['bill'].values()))
    print('\033[1;31;40m您的总额度为 %.2f RMB\033[0m'%data['balance'])
    if data['arrears'] > 0:     # 当账户卡内有余额时
        print('\033[1;31;40m已消费 0 RMB，余额 %.2f RMB\033[0m'%data['arrears'])
    else:
        print('\033[1;31;40m已消费 %.2f RMB\033[0m'%abs(data['arrears']))
    print('\033[1;31;40m剩余额度 %.2f RMB\033[0m'%(data['balance']+data['arrears']))
    if data['arrears'] >= 0:
        print('当前暂无欠款')
    else:
        print('您的消费流水：')
        for kind,things in data['bill'].items():
            if kind == 'trans':
                print('\033[32;1m转账\033[0m')
                for thing in things:
                    print('%s 转给账户 %s \033[32;1m%.2f RMB\033[0m'%(thing['time'],thing['target'],thing['price']))
            elif kind == 'draw':
                print('\033[32;1m取款\033[0m')
                for thing in things:
                    print('%s 取款 \033[32;1m%.2f RMB\033[0m'%(thing['time'],thing['price']))
            else:   # 商场消费
                print('\033[32;1m商场购物\033[0m')
                for thing in things:
                    print('%s 购入商品 %s 价格：\033[32;1m%.2f RMB\033[0m'%(thing['time'],thing['name'],thing['price']))
        print('\033[1;31;40m当前剩余额度 %.2f RMB\033[0m'%(data['balance']+data['arrears']))

    account_data.dump(data)
    return data


def repay(data):
    '''
    用户还款
    :param data: 用户数据
    :return: 返回最新的数据
    '''
    # data = account_data.load(data['id'])
    if data['arrears'] >= 0 and data['bill'] == {}:
        print('您目前没有待还款的账单')
    else:
        print('\033[31;1m您目前有 %.2f RMB待还\033[0m'%abs(data['arrears']))
        cash = input('请输入还款金额：').strip()
        while not cash.isdigit():
            print('\033[31;1m错误，只能是数字\033[0m')
            cash = input('请输入还款金额：').strip()
        else:
            data['arrears'] += int(cash)
            if data['arrears'] >= 0:
                print('\033[32;1m恭喜您，您已无欠款记录\033[0m')
                data['bill']['draw'] = []
                data['bill']['trans'] = []
                data['bill']['shop'] = []
                atm_log.info('account-%s has no arrears'%data['id'])
            else:
                print('\033[31;1m您目前有 %.2f RMB待还\033[0m'%abs(data['arrears']))
    account_data.dump(data)
    return data

def consume(data,types):
    '''
    用户消费
    :param data: 用户数据
    :param types: 消费类型，有取现draw,转账transfer,购物shop
    :return: 返回最新的用户数据
    '''
    # data = account_data.load(data['id'])
    if data['status'] == 1:
        print('\033[31;1m您的账户已被冻结，请及时还清欠款之后联系管理员解冻\033[0m')
        logging.error('freeze account-%s is doing consumer operations'%data['id'])
        return data
    elif data['balance'] + data['arrears'] >= 0:
        if types == 'trans':     # 转账
            target = input('请输入待转账账户的卡号：').strip()
            target_data = account_data.load(target)
            cash = input('请输入转账金额：').strip()
            while not cash.isdigit() or not target_data or target == data['id']:
                print('\033[31;1m错误，转账账户不存在或者金额不为数字，且不能转给自己\033[0m')
                target = input('请输入待转账账户的卡号：').strip()
                target_data = account_data.load(target)
                cash = input('请输入转账金额：').strip()
            else:
                if data['balance'] < abs(data['arrears'])+int(cash)*(1+0.05):
                    print('\033[31;1m超出可用额度')
                else:
                    print('转出账户：%s'%data['id'])
                    print('到达账户：%s'%target)
                    chos = input('yes/no?: ')
                    if chos in ('yes','y','Y'):
                        data['arrears'] -= int(cash)*(1+0.05)
                        target_data['arrears'] += int(cash)
                        print("\033[32;1m成功转账 %s 到账户 %s\033[0m"%(cash,target))
                        data['bill']['trans'].append({'time':str(datetime.datetime.now()),'target':target,'price':int(cash)})
                        atm_log.info('accout-%s transfer %.2f RMB to account-%s '%(data['id'],int(cash),target))
                    else:
                        print('交易取消')
            account_data.dump(data)
            account_data.dump(target_data)
            return data

        elif types == 'draw':        # 取现
            cash = input('请输入取款金额：').strip()
            while not cash.isdigit():
                print('\033[31;1m错误，只能是数字\033[0m')
                cash = input('请输入取款金额：').strip()
            else:
                if data['balance'] < abs(data['arrears'])+int(cash)*(1+0.05):
                    print('\033[31;1m超出可用额度\033[0m')
                else:
                    print('正在点钞，请稍候')
                    data['arrears'] -= int(cash)*(1+0.05)
                    print('\033[32;1m成功取款 %.2f RMB\033[0m'%int(cash))
                    data['bill']['draw'].append({'time':str(datetime.datetime.now()),'price':int(cash)})
                    atm_log.info('accout-%s draw %.2f RMB'%(data['id'],int(cash)))
            account_data.dump(data)
            return data

        elif types == 'shop':   # 商场购物
            price = 0
            for product in data['cart']:
                price += product['price']
            print('您的总额度为 %.2f RMB'%data['balance'])
            # 当arrears参数为正数，且账单参数内各数据的值为空时，最大可用额度为固定额度
            # 因为存在arrears参数是别人转账过来的，成了正数，但是账单并没有还清的可能
            if data['arrears'] > 0 and list(data['bill'].values()) == [[], [], []]:
                print('\033[32;1m可用额度为 %.2f RMB\033[0m'%data['balance'])
            else:
                print('\033[32;1m可用额度为 %.2f RMB\033[0m'%(data['balance'] + data['arrears']))
            while data['balance'] + data['arrears'] - price < 0:
                print('\033[32;1m总计为 %.2f RMB\033[0m'%price)
                ent = input('您的额度不足以支付以上商品，您是否要删除一些商品：yes/no:').strip()
                if ent in ('yes','y','Y'):
                    for index,product in enumerate(data['cart']):
                        print('编号 %s 商品名称 %s 商品价格 %s'%(index+1,product['name'],product['price']))
                    while True:
                        inde = input('请输入要删除的商品编号(务必为数字,输入“b”返回上一级)：').strip()
                        if inde in ('b','B','q',"q"):
                            break
                        elif inde.isdigit():
                            if data['cart']:
                                goods = data['cart'].pop(int(inde)-1)
                                price -= goods['price']
                                print('已删除商品 %s'%goods['name'])
                            else:
                                print('您的购物车已无商品')
                                break
                        else:
                            print('\033[31;1m输入有误\033[0m')
                else:
                    print('取消删除商品')
                    break
            else:   # 更新用户数据
                print('\033[1;31;40m总计消费 %.2f RMB\033[0m'%price)
                data['arrears'] -= price
                now = datetime.datetime.now().strftime('%Y-%d-%m %I:%M:%S %p')
                for someone in data['cart']:
                    someone['time']= now
                    data['bill']['shop'].append(someone)
                # 已结算后的数据恢复到初始状态
                data['cart'] = []
                account_data.dump(data)
                print('您已购买以上商品')
                print('\033[32;1m您的可用额度为 %.2f RMB\033[0m'%(data['balance'] + data['arrears']))
                return data
    else:
        print('\033[31;1m您的额度已用完\033[0m')


def transfer(data):
    '''
    用户转账
    :param data: 用户数据
    :return: 返回最新的用户数据
    '''
    data = consume(data,'trans')
    return data

def draw(data):
    '''
    用户取现
    :param data: 用户数据
    :return: 返回最新的用户数据
    '''
    data = consume(data,'draw')
    return data

def shop(data):
    '''
    用户购物
    :param data: 用户数据
    :return: 返回最新的用户数据
    '''
    data = consume(data,'shop')
    return data

def out(data):
    '''
    退卡退出
    :param data: 用户数据
    :return:
    '''
    print('正在退卡，请稍候')
    print('请取走您的银行卡')
    exit()

