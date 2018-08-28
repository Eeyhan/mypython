#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
import pickle,hashlib,time
import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from conf import settings
from lib import load_data
db_path = settings.db_path

# 父类，提供保存数据的功能
class Base:
    def save(self,identity):
        f = open(os.path.join(db_path,identity,str(self.id)),'wb')
        pickle.dump(self,f)
        f.close()

# 管理员类
class _Admin(Base):
    def __init__(self,username):
        hashobj = hashlib.md5()
        hashobj.update(str(time.time()).encode('utf-8'))
        self.id = hashobj.hexdigest()
        self.admin_name = username.replace(' ','')
    def reigister(self):
        password = input('密码: ').strip().replace(' ','')
        self.password = password
        self.level = '0'  # 等级为0表示管理员

# 课程类
class Course(Base):
    def __init__(self,course_name,cycle,price,campus):
        hashobj = hashlib.md5()
        hashobj.update(str(time.time()).encode('utf-8'))
        self.id = hashobj.hexdigest()                               # 课程id
        self.course_name = course_name.replace(' ','').lower()      # 课程名称
        self.cycle = cycle                                          # 周期
        self.price = price                                          # 学费
        self.campus = campus                                        # 校区

# 班级类
class Classes(Base):
    def __init__(self,classes_name,campus):
        hashobj = hashlib.md5()
        hashobj.update(str(time.time()).encode('utf-8'))
        self.id = hashobj.hexdigest()                               # 班级id
        self.classes_name = classes_name.replace(' ','').lower()    # 班级名称

# 讲师类
class Teacher(Base):
    def __init__(self,teacher_name,salary):
        hashobj = hashlib.md5()
        hashobj.update(str(time.time()).encode('utf-8'))
        self.id = hashobj.hexdigest()                               # 讲师id
        self.teacher_name = teacher_name.replace(' ','').lower()    # 讲师姓名
        self.salary = salary                                        # 工资
        self.balance = 0                                            # 余额
    def reigister(self):
        password = input('请输入密码：').strip()
        self.password = password
        self.level = '1'  # 等级1表示讲师

# 学校类
class School(Base):
    # __isinstance = None
    school_name = 'XX学院'
    def __init__(self,campus):
        hashobj = hashlib.md5()
        hashobj.update(str(time.time()).encode('utf-8'))
        self.id = hashobj.hexdigest()                           # 学校id
        self.campus = campus.replace(' ','').lower()            # 校区

# 学生类
class Student(Base):
    def __init__(self,student_name,age):
        hashobj = hashlib.md5()
        hashobj.update(str(time.time()).encode('utf-8'))
        self.id = hashobj.hexdigest()                               # 学生id
        self.student_name = student_name.replace(' ','').lower()    # 学生名字
        self.age = age                                              # 年龄
        self.score = 0                                              # 成绩，默认为0
    def reigister(self):
        password = input('请输入密码：').strip()
        self.password = password
        self.level = '2'      # 等级2表示学生

# 检查创建时的关键词参数数据是否已存在
def check_data(keyword,inputkeyword):
    tempdata = []
    count = 0
    for i in os.listdir(settings.data_path[keyword]):
        f = open(os.path.join(settings.data_path[keyword],i),'rb')
        tempdata.append(pickle.load(f))
    if tempdata:
        for i in tempdata:
            if inputkeyword  in i.__dict__.values():
                count += 1
    return count

# 创建管理员
def create_admin():
    username = input('用户名: ').strip()
    while not username:
        print('\033[31;1m数据不能为空\033[0m')
        username = input('用户名: ').strip()
    if not check_data('admin',username):
        admin = _Admin(username)
        admin.reigister()
        admin.save('admin')
        print('\033[32;1m创建管理员账号成功\033[0m')
    else:
        print('\033[31;1m已存在相同数据\033[0m')

# 创建学校
def  create_school(campus):
    campus_tuple = ('北京','上海')
    if campus in campus_tuple:
        if not check_data('school',campus):
            school = School(campus)
            school.save('school')
            print('\033[32;1m创建学校成功\033[0m')
        else:
            print('\033[31;1m已存在相同数据\033[0m')
    else:
        print('\033[31;1m目前我们只有北京和上海两个校区\033[0m')

# 创建课程
def create_course(campus):
    if campus == '北京':
        course_name = input('课程名称：').strip().replace(' ','').lower()
        while not course_name:
            print('\033[31;1m数据不能为空\033[0m')
            course_name = input('课程名称：').strip().replace(' ','').lower()
        while course_name not in ('python','Python','linux','Linux'):
            print('\033[31;1m北京校区只有Python和linux课程\033[0m')
            course_name = input('课程名称：').strip().replace(' ','').lower()
    elif campus == '上海':
        course_name = input('课程名称：').strip().replace(' ','').lower()
        while not course_name:
            print('\033[31;1m数据不能为空\033[0m')
            course_name = input('课程名称：').strip().replace(' ','').lower()
        while course_name not in ('go','Go','GO','golang'):
            print('\033[31;1m上海校区只有go课程\033[0m')
            course_name = input('课程名称：').strip().replace(' ','').lower()
    if not check_data('course',course_name):
        cycle = input('周期：').strip()
        price = input('学费：').strip()
        course = Course(course_name,cycle,price,campus)
        course.save('course')
        print('\033[32;1m创建课程成功\033[0m')
    else:
        print('\033[31;1m已存在相同数据\033[0m')

# 创建讲师
def create_teacher():
    print('''\033[1;31;40m注意：本系统已做了数据匹配筛选处理，在下面的创建讲师中，\n
讲师创建好则地区固定，请周密考虑，避免在创建班级时造成班级无法关联讲师的后果\033[0m''')
    time.sleep(3)
    teacher_name = input('讲师姓名：').strip().replace(' ','').lower()
    while not teacher_name:
        print('\033[31;1m数据不能为空\033[0m')
        teacher_name = input('讲师姓名：').strip().replace(' ','').lower()
    if not check_data('teacher',teacher_name):
        salary = input('工资：').strip()
        teacher = Teacher(teacher_name,salary)
        print('\033[33;1m请选择所属校区\033[0m')
        schoolobj = load_data.print_choice_data('school')
        while not  schoolobj:
            print('数据不能为空')
            schoolobj = load_data.print_choice_data('school')
        teacher.schoolobj = schoolobj
        teacher.reigister()
        teacher.save('teacher')
        print('\033[32;1m创建讲师成功\033[0m')
    else:
        print('\033[31;1m已存在相同数据\033[0m')


# 创建班级
def create_classes(campus):
    classes_name = input('班级名称：').strip().replace(' ','').lower()
    while not classes_name:
        print('\033[31;1m数据不能为空\033[0m')
        classes_name = input('班级名称：').strip().replace(' ','').lower()
    if not check_data('classes',classes_name):
        classes = Classes(classes_name,campus)
        print('\033[32;1m请选择课程\033[0m')
        courseobj = load_data.print_choice_data('course')
        while not  courseobj:
            print('\033[31;1m数据不能为空\033[0m')
            print('\033[32;1m请选择课程\033[0m')
            courseobj = load_data.print_choice_data('course')
        if 'python' in classes_name:
            while courseobj.course_name != 'python':
                print('\033[31;1m请选择匹配班级名称的课程\033[0m')
                courseobj = load_data.print_choice_data('course')
        elif 'linux' in classes_name:
            while courseobj.course_name != 'linux':
                print('\033[31;1m请选择匹配班级名称的课程\033[0m')
                courseobj = load_data.print_choice_data('course')
        elif 'go' in classes_name:
            while courseobj.course_name != 'go':
                print('\033[31;1m请选择匹配班级名称的课程\033[0m')
                courseobj = load_data.print_choice_data('course')

        print('\033[32;1m请选择讲师\033[0m')
        teacherobj = load_data.print_choice_data('teacher')
        while not teacherobj:
            print('\033[31;1m数据不能为空\033[0m')
            print('\033[32;1m请选择讲师\033[0m')
            teacherobj = load_data.print_choice_data('teacher')

        while  courseobj.campus != teacherobj.schoolobj.campus:
            print('\033[31;1m您选的讲师和课程不在同一个校区，请重新选择\033[0m')
            print('\033[32;1m您刚才选择的课程 %s 在 %s 校区\033[0m'%(courseobj.course_name,courseobj.campus))
            teacherobj = load_data.print_choice_data('teacher')

        classes.courseobj = courseobj       # 班级关联课程
        classes.teacherobj = teacherobj     # 班级关联讲师
        teacherobj.classesobj = classes     # 讲师关联班级
        classes.save('classes')
        teacherobj.save('teacher')
        print('\033[32;1m创建班级成功\033[0m')
    else:
        print('\033[31;1m已存在相同数据\033[0m')

# 创建学生
def create_student():
    student_name = input('您的名字：').strip().replace(' ','').lower()
    while not student_name:
        print('\033[31;1m数据不能为空\033[0m')
        student_name = input('您的名字：').strip().replace(' ','').lower()
    if not check_data('student',student_name):
        age = input('您的年龄：').strip()
        while not age.isdigit():
            print('\033[31;1m年龄必须是数字1以上的\033[0m')
            age = input('您的年龄：').strip()
        student = Student(student_name,age)
        student.reigister()
        balance = input('请输入您的存款额度：').strip()
        while not balance.isdigit():
            print('金额必须是数字')
            balance = input('请输入您的存款额度：').strip()
        student.balance = int(balance)
        print('\033[32;1m请选择所属校区：\033[0m')
        schoolobj = load_data.print_choice_data('school')         # 学校对象
        while not  schoolobj:
            print('\033[31;1m数据不能为空\033[0m')
            print('\033[32;1m请选择所属校区：\033[0m')
            schoolobj = load_data.print_choice_data('school')

        print('\033[32;1m请选择班级：\033[0m')
        classesobj = load_data.print_choice_data('classes')       # 班级对象
        while not classesobj:
            print('\033[31;1m数据不能为空\033[0m')
            print('\033[32;1m请选择班级：\033[0m')
            classesobj = load_data.print_choice_data('classes')
        while schoolobj.campus != classesobj.teacherobj.schoolobj.campus:
            print('\033[31;1m您选的班级与校区不匹配\033[0m')
            print('%s 在 %s校区'%(classesobj.classes_name,classesobj.teacherobj.schoolobj.campus))
            classesobj = load_data.print_choice_data('classes')
        student.schoolobj = schoolobj       # 学员关联学校校区
        student.classesobj = classesobj     # 关联班级
        student.pay_status = 1              # 付款状态，1表示未付款，0表示已付款
        student.save('student')
        print('\033[32;1m创建成功\033[0m')
    else:
        print('\033[31;1m已存在相同数据\033[0m')

# 修改数据
def update_data(keyword):
    print('请对下面每一项输入新的值，如果觉得对的不用改可直接回车，该项不作更改')
    choiceobj = load_data.print_choice_data(keyword)
    if choiceobj:
        # 重新取一遍是保证数据的时效性
        f = open(os.path.join(settings.data_path[keyword],choiceobj.id),'rb')
        pickdata = pickle.load(f)
        f.close()
        if keyword == 'school':
            campus = input('所属校区: ').strip().replace(' ','').lower()
            while campus not in ('北京','上海'):
                print('\033[31;1m目前我们学院只有北京和上海两个校区\033[0m')
                campus = input('所属校区: ').strip().replace(' ','').lower()
            pickdata.campus = campus
        elif keyword == 'classes':
            campus = input('班级所属校区: ').strip().replace(' ','').lower()
            while campus not in ('北京','上海'):
                print('\033[31;1m目前我们学院只有北京和上海两个校区\033[0m')
                campus = input('班级所属校区: ').strip().replace(' ','').lower()
            pickdata.campus = campus
            classes_name = input('班级名称：').strip().replace(' ','').lower()
            pickdata.classes_name = classes_name
        elif keyword == 'course':
            campus = input('课程所属校区: ').strip().replace(' ','').lower()
            while campus not in ('北京','上海'):
                print('\033[31;1m目前我们学院只有北京和上海两个校区\033[0m')
                campus = input('课程所属校区: ').strip().replace(' ','').lower()
            pickdata.campus = campus
            course_name = input('课程名称：').strip().replace(' ','').lower()
            cycle = input('周期：').strip()
            price = input('价格：').strip()
            pickdata.course_name = course_name
            pickdata.cycle = cycle
            pickdata.price = price
        elif keyword == 'teacher':
            campus = input('讲师所属校区: ').strip().replace(' ','').lower()
            while campus not in ('北京','上海'):
                print('\033[31;1m目前我们学院只有北京和上海两个校区\033[0m')
                campus = input('所属校区: ').strip().replace(' ','').lower()
            pickdata.campus = campus
            teacher_name = input('讲师姓名：').strip().replace(' ','').lower()
            salary = input('工资：').strip()
            pickdata.teacher_name = teacher_name
            pickdata.salary = salary
        pickdata.save(keyword)
        print('修改成功')
    else:
        print('您未作任何更改')

# 查看学校
def show_school():
    data_list = load_data.load_data('school')
    for i in data_list:
        print('-------------- 学校 ----------------')
        print('id:%s'%i.id)
        print('学校名称:%s'%i.school_name)
        print('学校校区:%s'%i.campus)
        print('------------------------------------')

# 查看讲师
def show_teacher():
    data_list = load_data.load_data('teacher')
    for i in data_list:
        print('-------------- 讲师 ----------------')
        print('id:%s'%i.id)
        print('姓名:%s'%i.teacher_name)
        print('工资:%s'%i.salary)
        print('所属校区:%s'%i.schoolobj.campus)
        print('------------------------------------')

# 查看课程
def show_course():
    data_list = load_data.load_data('course')
    for i in data_list:
        print('-------------- 课程 ----------------')
        print('id:%s'%i.id)
        print('课程名:%s'%i.course_name)
        print('周期:%s'%i.cycle)
        print('学费:%s'%i.price)
        print('------------------------------------')

# 查看班级
def show_classes():
    data_list = load_data.load_data('classes')
    for i in data_list:
        print('-------------- 班级 ----------------')
        print('id:%s'%i.id)
        print('班级名称:%s'%i.classes_name)
        print('课程名称:%s'%i.courseobj.course_name)
        print('讲师名称:%s'%i.teacherobj.teacher_name)
        print('------------------------------------')

# 查看学生
def show_student():
    data_list = load_data.load_data('student')
    for i in data_list:
        print('-------------- 学生 ----------------')
        print('id:%s'%i.id)
        print('学生姓名:%s'%i.student_name)
        print('所属校区:%s'%i.schoolobj.school_name)
        print('所学课程:%s'%i.courseobj.course_name)
        print('课程成绩:%s'%i.score)
        print('------------------------------------')
