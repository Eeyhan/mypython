#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from lib import load_data
from lib import logginer

# 创建日志对象
student_log = logginer.mylog('student')


# 交学费
def pay(userdata):
    bill = userdata.classesobj.courseobj.price
    inp = input('您报的课程价格为 %s RMB, 您是否要支付学费：[yes/no] '%bill).strip()
    if inp in ('yes','y','Y'):
        userdata.balance -= int(userdata.classesobj.courseobj.price)
        userdata.pay_status = 0     # 表示已付款
        userdata.save('student')
        print('\033[32;1m您已缴纳学费，成功报名\033[0m')
    else:
        print('您已取消付款，未付款的话您无法进行学习，无法享受我们承诺的待遇哦')
# 查看所有校区
def show_school(userdata):
    data_list = load_data.load_data('school')
    for i in data_list:
        print('-------------- 学校 ----------------')
        print('学校名称:%s'%i.school_name)
        print('学校校区:%s'%i.campus)
        print('------------------------------------')

# 查看所有课程
def show_course(userdata):
    data_list = load_data.load_data('course')
    for i in data_list:
        print('-------------- 课程 ----------------')
        print('课程名:%s'%i.course_name)
        print('周期:%s'%i.cycle)
        print('学费:%s'%i.price)
        print('------------------------------------')

# 查看所有讲师
def show_teacher(userdata):
    data_list = load_data.load_data('teacher')
    for i in data_list:
        print('-------------- 讲师 ----------------')
        print('姓名:%s'%i.teacher_name)
        print('所属校区:%s'%i.schoolobj.campus)
        print('------------------------------------')

# 查看所有班级
def show_classes(userdata):
    data_list = load_data.load_data('classes')
    for i in data_list:
        print('-------------- 班级 ----------------')
        print('班级名称:%s'%i.classes_name)
        print('课程名称:%s'%i.courseobj.course_name)
        print('讲师名称:%s'%i.teacherobj.teacher_name)
        print('------------------------------------')

# 查看个人信息
def show_myself(userdata):
    if userdata.pay_status == 1:
        print('\033[33;1m您还未交付学费\033[0m')
    print('姓名 %s - 年龄 %s - 所在校区 %s - 所在班级 %s 课程成绩 %s - 余额 %.2f\
'%(userdata.student_name,userdata.age,userdata.schoolobj.campus,userdata.classesobj.classes_name,userdata.score,userdata.balance))

def student(userdata=None):
    d = '''

    1.查看个人信息
    2.学费付费
    3.查看学校校区
    4.查看所有课程
    5.查看所有班级
    6.查看所有讲师
    '''

    d_func = {
        '1':show_myself,
        '2':pay,
        '3':show_school,
        '4':show_course,
        '5':show_classes,
        '6':show_teacher,
    }
    while True:
        print('\033[32;1m注意：请先创建好数据再作查看数据操作\033[0m')
        print(d)
        inp = input('(输入“q”退出)>>>: ').strip()
        if inp in ('q','Q','quit'):break
        elif inp in d_func:
            d_func[inp](userdata)
        else:
            print('输入有误')

if __name__ == '__main__':
    student()