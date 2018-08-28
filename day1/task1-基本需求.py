#!/usr/bin/env python
# -*- coding:utf-8 -*-






# _username = 'lily'
# _password = '123'
#
# username = input("请输入您的账号：")
# password = input("请输入您的密码：")
#
# count = 0
# while username != _username or password != _password:
#     count += 1
#     if count<3:
#         print('登录失败! 请重新登录，您还有 %s 次机会'%(3-count))
#         username = input("请输入您的账号：")
#         password = input("请输入您的密码：")
#     else:
#         print("您已尝试三次仍登录失败")
#         break
#
# else:
#     print('恭喜您，登录成功')
# print('-----程序结束----------')


#
# _name = ('seven','alex')
# _password = '123'

# count = 0
# while count<3:
#      username = input('请输入您的账号名：')
#      password = input("请输入您的密码：")
#      if username in _name and password == _password:
#           print('登录成功')
#           break
#      else:
#           print('登录失败')
#      count += 1
# else:
#      print('您已尝试三次登录，仍错误')



name = input("请输入您的名字：").strip()
age = input("请输入您的年龄：").strip()
doing = input('在做什么：').strip()
print('我叫'+name+','+age+'岁,'+'我正在'+doing)
