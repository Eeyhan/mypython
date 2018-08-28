#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

menu = {
    '北京':{
        '海淀':{
            '五道口':{
                'soho':{},
                '网易':{},
                'google':{}
            },
            '中关村':{
                '爱奇艺':{},
                '汽车之家':{},
                'youku':{},
            },
            '上地':{
                '百度':{},
            },
        },
        '昌平':{
            '沙河':{
                '老男孩':{},
                '北航':{},
            },
            '天通苑':{},
            '回龙观':{},
        },
        '朝阳':{},
        '东城':{},
    },
    '上海':{
        '闵行':{
            "人民广场":{
                '炸鸡店':{}
            }
        },
        '闸北':{
            '火车站':{
                '携程':{}
            }
        },
        '浦东':{},
    },
    '山东':{},
}

# temp作为临时存储，实现动态循环
# parent作为父级列表
temp = menu
parent = []
while True:
    if temp == {}:
        print('此级暂无数据，您可以退出或回到上一级')
    for i in temp:
        print(i)                            # 打印选项
    chos = input("请输入(输入“q”退出，输入“b”回到上一级)>>>：").strip()
    if len(chos) == 0:print('输入不能为空，请重新输入！')
    if chos in temp:
        parent.append(temp)                 # 将父级目录暂存
        temp = temp[chos]                   # 更新临时存储变量，下次循环自动进入子级
    elif chos in ('q','quit','Q','exit'):
        print('您已退出')
        break
    elif chos in ('b','B','back'):          # 回到父级（上一级）
        print('您已回到上级')
        temp = parent.pop()                 # 恢复、取出父级（上一级）
    else:
        print('此级目录无此地名 “%s” ,请重新输入！'%chos)

