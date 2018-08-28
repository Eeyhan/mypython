#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan



# 打开文件并临时存储数据

f = open('listdata','r')
data = eval(f.read())
# data数据为：[['lily', 0, '123'], ['nero', 0, '111'], ['jack', 0, '121']]
# 内层列表内，
f.close()


# 提示语
print("请登录，您共有 3 次机会")
username = input("请输入您的账号：")
password = input("请输入您的密码：")


# data数据为：[['lily', 0, '123'], ['nero', 0, '111'], ['jack', 0, '121']]
user1,user2,user3 = data # 将data数据内的三个列表分别赋值
# user1[0] 为账号名
# user1[1] 为状态
# user1[2] 为密码

'其实这里有个局限，如果文件数据超过三个或者少于三个则不适用，后期可以解决'
count = 1  # 计数器

while count<3:
    count += 1
    if username not in  (user1[0],user2[0],user3[0]): # 输入的账号都不在数据内时
        print('登录失败，请重新登录,您还有 %s 次机会'%(4-count))
        username = input("请输入您的账号：")
        password = input("请输入您的密码：")

    elif username == user1[0]:
        if user1[1] == 1:        # 状态为1表示锁定状态，无法正常使用
            print("该账户已锁定，无法正常使用")
            break
        elif password == user1[2]:
            print('恭喜您，登录成功')
            break
        else:
            print('登录失败，请重新登录,您还有 %s 次机会'%(4-count))
            username = input("请输入您的账号：")
            password = input("请输入您的密码：")
    elif username == user2[0]:
        if user2[1] == 1:
            print("该账户已锁定，无法正常使用")
            break
        elif password == user2[2]:
            print('恭喜您，登录成功')
            break
        else:
            print('登录失败，请重新登录,您还有 %s 次机会'%(4-count))
            username = input("请输入您的账号：")
            password = input("请输入您的密码：")

    elif username == user3[0]:
        if user3[1] == 1:
            print("该账户已锁定，无法正常使用")
            break
        elif password == user3[2]:
            print('恭喜您，登录成功')
            break
        else:
            print('登录失败，请重新登录,您还有 %s 次机会'%(4-count))
            username = input("请输入您的账号：")
            password = input("请输入您的密码：")

else:
    print("您已尝试 3 次仍登录失败")
    if username == user1[0]:
        user1[1] = 1 #状态为1表示锁定状态，错误登录三次，将该账户状态设置为锁定
        print("原因：账户已锁定")
    if username == user2[0]:
        user2[1] = 1
        print("原因：账户已锁定")
    if username == user3[0]:
        user3[1] = 1
        print("原因：账户已锁定")
    else:
        print("原因：不存在的用户名")


data = [user1,user2,user3]
f = open("listdata",'w')
f.write(str(data))  #以字符串的形式把最新的写入文件内存储
f.close()

print('-----程序结束----------')