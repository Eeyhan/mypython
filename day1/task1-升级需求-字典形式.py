#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

f = open('dictdata','r')
data = eval(f.read())

# data 数据为：{'lily': {'status': 0, 'password': '123'}, 'nero': {'status': 0, 'password': '111'}, 'jack': {'status': 0, 'password': '121'}}

f.close()
print("请登录，您共有 3 次机会")
username = input("请输入您的账号：")
password = input("请输入您的密码：")

count = 0   #作计数器
while username not in  data.keys() or password != data[username]["password"]:
    count += 1
    if count<3:
        print('登录失败! 请重新登录，您还有 %s 次机会'%(3-count))
        username = input("请输入您的账号：")
        password = input("请输入您的密码：")
    elif username in data.keys():           #当用户名存在数据库内时
        data[username]["status"] = 1        #状态1表示锁定
        print("您已尝试 3 次仍登录失败,账户已锁定")
        break
    else:                                   #当用户名不存在数据库内时
        print("原因：不存在的用户名")
        break
else:
    if data[username]["status"] == 1:       #当用户名已锁定状态不能作登录操作
        print("该账户已锁定，无法正常登录")
    else:
        print('恭喜您，登录成功')

# 更新数据
f = open('dictdata','w')
f.write(str(data))
f.close()

print('-----程序结束----------')