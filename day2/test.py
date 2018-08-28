#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan



#
# li = ['alex', 'eric', 'rain']
# s= '_'
# print(s.join(li))

# li = ["alec", " aric", "Alex", "Tony", "rain"]
# tu = ("alec", " aric", "Alex", "Tony", "rain")
# dic = {'k1': "alex", 'k2': ' aric', "k3": "Alex", "k4": "Tony"}
#
# print(dic)
# tempdic = {}
# for i in dic:
#     tempkey = i.strip()
#     tempdic[tempkey] = dic[i].strip()
# dic = tempdic
# print(dic)
#
# li = ['alex', 'eric', 'rain']
# # print(len(li))
# li.append("seven")
#
#
# li.insert(0,"Tony")
# li.insert(1,"Kelly")
# li.remove("eric")
# print(li.pop(1))
# li.pop(2)
# del li[2:5]
# li.reverse()
# for i in range(0,len(li)):
#     print(i , li[i])

# for i,j in enumerate(li,100):
#     print(i ,j)
#
# li = ["hello", 'seven', ["mon", ["h", "kelly"], 'all'], 123, 446]
#
# li[2][2] = li[2][2].upper()
# print(li)
#
# tu = ('alex', 'eric', 'rain')
# for i,j in enumerate(tu,10):
#     print(i,j)

# tu = ("alex", [11, 22, {"k1": 'v1', "k2": ["age", "name"], "k3": (11,22,33)}, 44])
# tu[1][2]["k2"].append("seven")
# print(tu)

# dic = {'k1': "v1", "k2": "v2", "k3": [11,22,33]}
# # for i in dic:
# #     print(dic[i])
# dic["k4"] = "v4"
# dic["k1"] = 'alex'
# dic['k3'].append(44)
# temp = {"k":"v"}
# temp.update(dic)
# print(temp)

# s = "alex"
# temp = tuple(s)
# print(temp)
# li = ["alex", "seven"]
# temp = {}
# num = 10
# for i in li:
#     temp[i] = num
#     num += 1
# print(temp)

# se ={11,22,33,44,55,66,77,88,99,90}
# temp = {"k1":[],"k2":[]}
# for i in se:
#     if i>66:
#         temp["k1"].append(i)
#     else:
#         temp["k2"].append(i)
# print(temp)

# li = {'1':'手机','2':'电脑','3':'鼠标'}
# for i,j in li.items():
#     print(i,'---',j)
# choice = input(">>> ")
# print(li[choice])

# l1 = [11,22,33]

# l2 = [22,33,44]

# print(set(l2).symmetric_difference(set(l1)))

# for i in range(0,101):
#     print(100-i,end="")

# num = 0
# while num<101:
#     print(100-num,end='_')
#     num+=1

# for i in range(1,10):
#     for j in range(1,10):
#         print("%sX%s = %s"%(i,j,i*j))

# s = "hello, world"
# print('\033[35m%s\033[0m' % s)
# print('\033[1;36;28m%s\033[0m' % s)
# print('\033[1;35;29m%s\033[0m' % s)
# print('\033[1;39;30m%s\033[0m' % s)
# print('\033[1;31;42masdfasfads\033[0m')
# print('\033[1;31;43masdfasfads\033[0m')
# print('\033[1;31;44masdfasfads\033[0m')
# print('\033[1;31;45masdfasfads\033[0m')
# print('\033[1;31;48masdfasfads\033[0m')
# print('\033[1;31masdfasfads\033[0m')
# print('\033[1;37;42m%s\033[0m' % s)
# print('\033[1;36;43m%s\033[0m' % s)