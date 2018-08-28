#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from conf import settings
from lib import main
from lib import load_data
from lib import logginer

# 创建日志对象
admin_log = logginer.mylog('admin')

# 单独创建课程
def create_course(admindata):
    campus = input('所属校区: ').strip()
    while campus not in ('北京','上海'):
        print('目前我们学院只有北京和上海两个校区')
        campus = input('所属校区: ').strip()
    main.create_course(campus)
    admin_log.info('%s create course'%admindata.admin_name)

# 单独创建校区
def create_school(admindata):
    campus = input('所属校区: ').strip()
    while campus not in ('北京','上海'):
        print('目前我们学院只有北京和上海两个校区')
        campus = input('所属校区: ').strip()
    main.create_school(campus)
    admin_log.info('%s create school'%admindata.admin_name)

# 单独创建班级
def create_classes(admindata):
    campus = input('所属校区: ').strip()
    while campus not in ('北京','上海'):
        print('目前我们学院只有北京和上海两个校区')
        campus = input('所属校区: ').strip()
    main.create_classes(campus)
    admin_log.info('%s create classes'%admindata.admin_name)

# 单独创建讲师
def create_teacher(admindata):
    main.create_teacher()
    admin_log.info('%s create teacher'%admindata.admin_name)

# 同时创建多个数据
def create_school_classes_course(admindata):
    try:
        inp = input('您是否要创建多条数据：[yes/no]').strip()
        if inp in ('q','Q','quit','exit','e','E'):return
        if inp in ('Yes','yes','y'):
            campus = input('创建学校校区:').strip().replace(' ','').lower()
            main.create_school(campus)
            print('\n\033[33;1m创建课程\033[0m\n')
            main.create_course(campus)
            print('\n\033[33;1m创建讲师\033[0m')
            main.create_teacher()
            print('\n\033[33;1m创建班级\033[0m')
            main.create_classes(campus)
            admin_log.info('%s create datas'%admindata.admin_name)
        else:
            print('\033[31;1m输入有误\033[0m')
    except (Exception,KeyboardInterrupt) as e:
        print('\033[31;1m操作异常，程序将回到初始状态\033[0m')
        print(e)
        # 原子型操作，回滚到初始状态
        for i in os.listdir(settings.data_path['school']):
            os.remove(os.path.join(settings.data_path['school'],i))

        for i in os.listdir(settings.data_path['teacher']):
            os.remove(os.path.join(settings.data_path['teacher'],i))

        for i in os.listdir(settings.data_path['student']):
            os.remove(os.path.join(settings.data_path['student'],i))

        for i in os.listdir(settings.data_path['classes']):
            os.remove(os.path.join(settings.data_path['classes'],i))

        for i in os.listdir(settings.data_path['course']):
            os.remove(os.path.join(settings.data_path['course'],i))

        for i in os.listdir(settings.data_path['admin']):
            os.remove(os.path.join(settings.data_path['admin'],i))

# 修改数据
def update_school_classes_course(admindata):
    keystype = ('school','course','classes','teacher')
    inp = input('请输入待修改的类型: [school/course/classes/teacher] ').strip()
    while inp not in keystype:
        if inp in ('q','Q','quit','exit','e','E'):break
        print('\033[31;1m操作异常，您的账号权限只可以修改学校、课程、班级、讲师的数据\033[0m')
        inp = input('请输入待修改的类型: [school/course/classes/teacher] ').strip()
    else:
        data = load_data.load_data(inp) #还未修改的数据
        try:
            main.update_data(inp)
            admin_log.info('%s update %s’ data'%(admindata.admin_name,inp))
        except Exception as e:
            print('\033[31;1m修改数据中途发生异常\033[0m')
            print(e)
            # 原子型操作，回滚到初始状态
            load_data.rollback_data(inp,data)

# 查看学校
def show_school(admindata):
    main.show_school()

# 查看课程
def show_course(admindata):
    main.show_course()

# 查看班级
def show_classes(admindata):
    main.show_classes()

#
def show_teacher(admindata):
    main.show_teacher()

# 管理员视图
def admin(admindata=None):
    tempdata = os.listdir(settings.data_path['student'])
    tempdata.extend(os.listdir(settings.data_path['classes']))
    tempdata.extend(os.listdir(settings.data_path['teacher']))
    tempdata.extend(os.listdir(settings.data_path['school']))
    tempdata.extend(os.listdir(settings.data_path['course']))
    if not tempdata:
        print('\033[33;1m检测到您的选课系统暂无任何数据\033[0m')
        create_school_classes_course(admindata)
    d = '''
        1.添加多条数据
        2.修改多条数据
        3.创建学校
        4.创建课程
        5.创建班级
        6.创建讲师
        7.查看学校
        8.查看班级
        9.查看课程
        10.查看讲师
    '''
    d_func = {
        '1':create_school_classes_course,
        '2':update_school_classes_course,
        '3':create_school,
        '4':create_course,
        '5':create_classes,
        '6':create_teacher,
        '7':show_school,
        '8':show_classes,
        '9':show_course,
        '10':show_teacher
    }

    while True:
        print('\033[32;1m注意：请先创建好数据再作查看数据操作\033[0m')
        print(d)
        chos = input('>>>: ').strip()
        if chos in ('Q','q','quit','exit'):break
        elif chos in d_func:
            d_func[chos](admindata)
        else:
            print('输入有误')
if __name__ == '__main__':
    admin()