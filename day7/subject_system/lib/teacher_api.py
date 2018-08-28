#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,pickle
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from conf import settings
from lib import load_data
from lib import logginer

# 创建日志对象
teacher_log = logginer.mylog('teacher')

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
    print('姓名：%s - 所在校区 %s - 管理班级 %s - 授课课程 %s - 工资 %s - 余额 %s'\
%(userdata.teacher_name,userdata.schoolobj.campus,userdata.classesobj.classes_name,userdata.classesobj.courseobj.course_name,userdata.salary,userdata.balance))

# 选择班级
def choice_classes(userdata):
    print('选择上课的班级')
    if userdata.classesobj:
        print('您已有管理的班级，无需再选择班级')
    else:
        classesobj = load_data.print_choice_data('classes')
        while not classesobj:
            print('\033[31;1m数据不能为空\033[0m')
            print('选择上课的班级')
            classesobj = load_data.print_choice_data('classes')
        userdata.classesobj = classesobj    # 讲师关联班级
        classesobj.teacherobj = userdata    # 班级关联讲师
        print('选择班级成功，您已成为该班级的任课老师')
        teacher_log.info('%s choose classes %s'%(userdata.teacher_name,classesobj.classes_name))
        userdata.save('teacher')

# 查看所管理的班级
def check_your_classes(userdata):
    classes = userdata.classesobj
    print('班级名称 %s - 所授课程 %s - 课程周期 %s - 学费 %s - 讲师 \
%s'%(classes.classes_name,classes.courseobj.course_name,classes.courseobj.cycle,classes.courseobj.price,userdata.teacher_name))

# 查看所管理的学员列表
def check_your_student(userdata):
    student_list = []
    data_list = load_data.load_data('student')
    if data_list:
        for i in data_list:
            if userdata.classesobj.classes_name == i.classesobj.classes_name:
                student_list.append(i)
    else:
        print('\033[33;1m目前暂无学员前来报名或者管理员还未及时更新数据，请耐心等待\033[0m')
    for index,i in enumerate(student_list):
        print('编号 %s 学员姓名 %s - 年龄 %s - 所在班级 %s - \
课程成绩 %s'%(index+1,i.student_name,i.age,i.classesobj.classes_name,i.score))
    return student_list

# 修改管理的学员成绩
def update_your_student(userdata):
    inp = input('您是否要修改学员成绩？[yes/no]').strip()
    if inp in ('yes','Y','y'):
        student_list = check_your_student(userdata)
        chos = input('请输入待修改学员的编号：').strip()
        while not chos.isdigit() or int(chos) > len(student_list) or int(chos) < 0:
            chos = input('\033[31;1m不存在编号 %s 对应的选项，请重新输入:\033[0m'%chos).replace(' ','').lower()
        else:
            newdata = student_list[int(chos)-1]
            # 重新取一遍是保证数据的时效性
            f = open(os.path.join(settings.data_path['student'],newdata.id),'rb')
            pickdata = pickle.load(f)
            f.close()
            score = input('新的成绩：').strip()
            while not score:
                print('\033[31;1m数据不能为空\033[0m')
                score = input('新的成绩：').strip()
            pickdata.score = score
            pickdata.save('student')
            teacher_log.info('%s update %s score'%(userdata.teacher_name,pickdata.student_name))
            print('\033[32;1m修改成绩成功\033[0m')
            userdata.balance += int(userdata.salary)        # 发放工资
            userdata.save('teacher')
    else:
        print('取消修改成绩')

def teacher(userdata=None):
    d = '''
    1.选择上课班级
    2.查看管理班级
    3.查看管理班级的所有学员
    4.修改学员成绩
    5.查看个人信息
    6.查看学校校区
    7.查看所有班级
    8.查看所有课程
    9.查看所有讲师
    '''
    d_func = {
        '1':choice_classes,
        '2':check_your_classes,
        '3':check_your_student,
        '4':update_your_student,
        '5':show_myself,
        '6':show_school,
        '7':show_classes,
        '8':show_course,
        '9':show_teacher
    }
    while True:
        print('\033[32;1m注意：请先创建好数据再作查看数据操作\033[0m')
        print(d)
        inp = input('(输入“q”退出)>>>: ').strip()
        if inp in ('q','Q','quit'):break
        elif inp in d_func:
            d_func[inp](userdata)
        else:
            print('\033[32;1m输入有误\033[0m')
if __name__ == '__main__':
    teacher()