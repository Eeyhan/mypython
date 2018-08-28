#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
print('------------欢迎光临XX购物商场-----------')
with open('userdata') as f:
    userdata = eval(f.read())
print("请登录")
# 检测登录
username = input("请输入您的账号：")
password = input("请输入您的密码：")
while username not in  userdata.keys() or password != userdata[username]['password']:
    print('登录失败！用户名或密码错误,请重新登录')
    username = input("请输入您的账号：")
    password = input("请输入您的密码：")
else:
    print('恭喜您，登录成功\n')
goods = [
{"name": "联想拯救者", "price": 6999},
{"name": "MACbook Air", "price": 6099},
{"name": "罗技鼠标", "price": 78},
{"name": "机械键盘", "price": 899},
{"name": "TP_link路由器", "price": 99},
{"name": "沐浴露", "price": 19.8},
{"name": "洗发露", "price": 21.4},
{"name": "液晶电视", "price": 4999},
{"name": "空调", "price": 3998},
{"name": "iphone8", "price": 4888},
{"name": "华为p20pro", "price": 4988},
{"name": "水杯", "price": 48},
{"name": "抽纸", "price": 3.8},
{"name": "扫地机器人", "price": 2999},
{"name": "蒙牛纯牛奶", "price": 69},
{"name": "伊利优酸乳", "price": 48},
{"name": "山地自行车", "price": 1088},
{"name": "小米代步车", "price": 1999},
{"name": "NIKE跑鞋", "price": 539},
]
if userdata[username]['balance']:       # 判断是否有账单记录
    balance = userdata[username]['balance']
else:
    balance = input('\n请输入您的工资：').strip()
    while  not balance.isdigit():
        print('工资不能为数字以外的其他字符，请重新输入')
        balance = input('\n请输入您的工资：').strip()
    else:
        balance = int(balance)
bill = []                               # 历史账单
while True:
    count = 0                           # 为商品编号
    print("------------商品清单------------")
    for i in goods:
        count += 1
        print('编号:',count,'商品:',i['name'],'--',i['price'],'￥')
    print("-------------------------------")
    chos = input('\n请输入物品编号(输入 “b” 查看历史账单，输入“q”退出)：').strip()

    if not chos.isdigit():             # 当输入的不是数字时
        if chos in ('b','B','bill'):   # 查看历史账单
            if userdata[username]["bill"]:
                print('---------您的历史账单------\n')
                for history in userdata[username]["bill"]:
                    print('商品:',history['name'],'--','价格:',history['price'],'￥')
                print('--------------------------\n')
            else:
                print('您暂无历史账单\n')
        elif chos in ('q','Q','quit'):   # 退出
            money = 0
            if len(bill):                # 如果有账单就打印当前账单
                print('---------您的购买清单------\n')
                for good in bill:
                    print('商品:',good['name'],'--','价格:',good['price'],'￥')
                    money += good['price']
                print('--------------------------\n')
            print('\033[1;31;40m总消费：%.2f ￥\033[0m'%money)
            print('\033[1;31;40m余额：%.2f ￥\033[0m'%balance)
            # 更新用户数据并存入文件
            userdata[username]['balance'] = balance
            userdata[username]['bill'].extend(bill)
            print('您已退出，欢迎下次光临')
            with open('userdata','w') as f:
                f.write(str(userdata))
            print('------------程序结束--------------------')
            break
        else:                   # 当输入的非数字，非退出，也非查看账单选项则提示
            print('请输入编号为1开始的数字，而非其他字符\n')
    else:                       # 当输入的为数字时
        chos = int(chos)
        if int(chos) < 0 or int(chos) > len(goods): # 当输入的数字不在编号范围内时
            print('输入有误，请重新选择,不存在编号为 “%s” 的商品\n'%chos)
        else:
            if balance < goods[chos-1]['price']:    # 当余额不足时
                print('\033[1;31m余额不足!\033[0m')
                print('\033[1;31;40m您的余额为 %.2f ￥，该商品为 %.2f ￥\033[0m\n'%(balance,goods[chos-1]['price']))
            else:                                   # 当余额足够时
                bill.append(goods[chos-1])          # 加入购物车
                balance -= goods[chos-1]['price']   # 更新余额
                print("\033[1;31;40m%s 已加入购物车\033[0m\n"%goods[chos-1]['name'])


