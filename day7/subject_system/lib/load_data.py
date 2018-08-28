#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
import os,sys,pickle
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from conf import settings

# 加载对应数据
def load_data(keyword):
    loads_data = []
    if keyword in ('classes','course','school','student','teacher','score','admin'):
        if os.listdir(os.path.join(settings.data_path[keyword])):
            for i in os.listdir(os.path.join(settings.data_path[keyword])):
                f = open(os.path.join(settings.data_path[keyword],i),'rb')
                loads_data.append(pickle.load(f))
                f.close()
    return loads_data

# 打印对应数据

def print_choice_data(keyword):
    loads_data = load_data(keyword)
    if loads_data != []:
        if keyword == 'school':
            for index,cont in enumerate(loads_data):
                print('编号：%s - 学校名称：%s - 所属校区 %s'%(index+1,cont.school_name,cont.campus))
        elif keyword == 'classes':
            for index,cont in enumerate(loads_data):
                print('编号：%s - 班级名称：%s - 所授课程 %s - 价格 %s - 讲师 %s - 所在校区 %s'%(index+1,cont.classes_name,cont.courseobj.course_name,cont.courseobj.price,cont.teacherobj.teacher_name,cont.courseobj.campus))
        elif keyword == 'course':
            for index,cont in enumerate(loads_data):
                print('编号：%s - 课程名称：%s - 学习周期 %s - 价格 %s'%(index+1,cont.course_name,cont.cycle,cont.price))
        elif keyword == 'teacher':
            for index,cont in enumerate(loads_data):
                print('编号：%s - 讲师名称：%s - 工资 %s - 所属校区 %s'%(index+1,cont.teacher_name,cont.salary,cont.schoolobj.campus))
        elif keyword == 'student':
            for index,i in enumerate(loads_data):
                print('编号 %s 学员姓名 %s - 年龄 %s - 所学课程 %s - \
课程成绩 %s'%(index+1,i.student_name,i.age,i.courseobj.course_name,i.score))

        inp = input('请输入数据的编号：').strip()
        if inp and inp.isdigit():
            while int(inp) > len(loads_data) or int(inp) < 0:
                inp = input('\033[31;1m不存在编号 %s 对应的选项，请重新输入\033[0m'%inp).replace(' ','').lower()
            choicedata = loads_data[int(inp)-1]
            return choicedata
    else:
        print('\033[31;1m数据为空\033[0m')

# 回滚函数
def rollback_data(keyword,data):
    for i in data:
        f = open(os.path.join(settings.data_path[keyword],i.id),'wb')
        pickle.dump(f,i)
        f.close()
