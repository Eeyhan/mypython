#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,json,logging
product_path = os.path.dirname(__file__)
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(product_path)
sys.path.append(base_path)

from atm.database import account_data
from atm.conf import settings
from atm.lib import transaction
from atm.lib import logger

# 所有账户数据
userdatas = account_data.load_all()
# 创建日志对象
mall_log = logger.mylog('mall')
data = None         # 临时存储当前登录账户的数据
cart = []           # 临时存储当前账户购物车数据
def cart_product(kind=None):
    '''
    查看商品并添加到购物车
    :param kind: 产品分类，默认为空
    :return:
    '''
    global data
    filepath = os.path.join(product_path,'products','products')
    f = open(filepath,encoding='utf-8')
    productdata = json.load(f)
    for type,produc in productdata.items():
        if kind == type:    # 当有传入参数时，打印对应分类产品
            print('\033[33;1m'+type+'类：\033[0m\n')
            for name,detail in produc.items():
                print(name,end=' - ')
                print('商品名：%s\t商品价格：%s'%(detail['name'],detail['price']))
            while True:
                choice = input('请输入您要购买的产品编号(输入“b”回到上一级)：').strip()
                if choice in ('b','B'):
                    data['cart'] = cart
                    account_data.dump(data)
                    return cart
                elif choice not in productdata[kind]:
                    print('\033[31;1m不存在编号为 %s 的商品，请重新选择\033[0m'%choice)
                else:
                    cart.append(productdata[kind][choice])
                    print('\033[32m%s 已加入购物车\033[0m'%productdata[kind][choice]['name'])
        elif kind == None:  # 当无传入参数时，默认打印所有产品
            print(type+'类：\n')
            for name,detail in produc.items():
                print(name,end=' - ')
                print('商品名：%s\t商品价格：%s'%(detail['name'],detail['price']))
def pay(userdata):
    '''
    支付函数,调用支付接口
    :param userdata: 用户数据
    :return:
    '''
    transaction.shop(userdata)

login_flag = False  # 验证登录参数
def login(func):
    def inner():
        global login_flag
        global data
        global cart
        if not login_flag:
            print('\033[31;1m检测到您尚未登录，请先登录\033[0m')
            username = input('账户: ').strip()
            password = input('密码: ').strip()
            for i in userdatas.values():
                if username == i['name']:
                    while password != i['password']:
                        print('\033[31;1m登录失败，密码错误，请重新登录\033[0m')
                        password = input('密码: ').strip()
                    else:
                        data = i

                        # 如果临时购物车参数为空且用户数据里购物车有数据时
                        if data['cart']:
                            cart = data['cart']
                        print('\033[32;1m恭喜您 %s 登录成功\033[0m'%(data['name']))
                        login_flag = True
                        balance = input('请输入您的额度：').strip()
                        if balance.isdigit():
                            # 当登录成功后输入的额度为数字且额度比默认的额度高时
                            if data['balance'] < float(balance):
                                data['balance'] = float(balance)
                        func()
                        mall_log.info('account-%s logined'%data['id'])
                        return data
            else:
                print('\033[31;1m不存在的账户名\033[0m')
        else:
            func()
            return data
    return inner
def home():
    '''
    商场主页
    :return:
    '''
    print('------------XX购物商场欢迎您--------------')
    print('水果生鲜区攀枝花芒果超值清仓大甩卖')
    print('小米8又有货啦，赶快抢')
    print('华为nova3亮眼发售')
    print('魅族16 J.wong倾力打造，限时预售')

@login
def phone_pc():
    '''
    手机电脑页面
    :return:
    '''
    cart_product('手机电脑')
@login
def eleproduc():
    '''
    家用电器页面
    :return:
    '''
    cart = cart_product('家用电器')
@login
def life():
    '''
    生活家居页面
    :return:
    '''
    cart = cart_product('生活家居')
@login
def dress():
    '''
    服饰箱包页面
    :return:
    '''
    cart = cart_product('服饰箱包')
@login
def fresh():
    '''
    牛奶生鲜页面
    :return:
    '''
    cart = cart_product('牛奶生鲜')
@login
def fruit():
    '''
    水果干货页面
    :return:
    '''
    cart = cart_product('水果干货')
@login
def shop_cart():
    '''
    购物车/付款结账页面
    :return:
    '''
    global cart
    price = 0
    if cart:        # 如果临时购物车参数或者用户数据内不会空时
        print('--------------')
        for i in cart:
            print('商品名：%s\t商品价格：%.2f'%(i['name'],i['price']))
            price += i['price']
        print('\033[1;31;40m总计为 %.2f RMB\033[0m'%price)
        print('--------------')
        inp = input('确认支付以上物品？yes/no: ')
        data['cart'] = cart   # 让临时购物车数据长期存入用户的购物车内
        if inp in ('yes','y','Y'):
            pay(data)
            cart = []         # 支付后临时购物车数据清零
            mall_log.info('account-%s on the mall shoped %.2f RMB'%(data['id'],price))
    else:                     # 用户数据内购物车无数据，且临时购物车参数也无数据
        print('您的购物车内暂无商品')

optiondict = {
    '1':home,
    '2':phone_pc,
    '3':eleproduc,
    '4':fresh,
    '5':fruit,
    '6':dress,
    '7':shop_cart
}
options = '''
1.首页
2.手机电脑
3.家用电器
4.牛奶生鲜
5.水果干货
6.服饰鞋包
7.购物车/付款结账'''

home()
while True:
    print(options)
    chos = input('(输入“q”退出)>>>: ').strip()
    if chos in ('q','Q','quit'):
        print('您已退出')
        break
    elif chos in optiondict:
        data = optiondict[chos]()
    else:
        print('\033[31;1m输入有误，请重试\033[0m')
print('-------------------end-------------------')