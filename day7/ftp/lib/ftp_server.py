#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,subprocess,struct

import socket,hashlib,json
from conf import settings
from lib import load_dump_data
from lib import logger

# 服务器对象
class ftp_server:
    def __init__(self,type):
        self.host = settings.host
        self.family = settings.family
        self.type = settings.prototal[type]
        self.base_path = settings.server_path
        self.path = None
        self.current_dir = None
        self.user = None
        self.logobj = logger.mylog('server')
    def create_ftp_sever(self):
        '''
        创建一个ftp服务器对象
        :return: 返回服务器对象
        '''
        self.server = socket.socket(self.family,self.type)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind(self.host)
        self.server.listen(8)   # 允许8个客户端同时访问
        self.logobj.info('create the server')
        return self.server

    def count_size(self,path):
        '''
        验证磁盘配额
        :param path:用户的家目录
        :return:    # 返回数据大小
        '''

        all_file = 0
        for i in os.listdir(path):
            temp_path = os.path.join(path,i)
            if os.path.isfile(temp_path):       # 如果是文件计算大小
                all_file += os.stat(os.path.join(path,i)).st_size
            elif os.path.isdir(temp_path):      # 如果是文件递归
                self.count_size(temp_path)
        return all_file

    def cd(self,dirs):
        '''
        切换目录
        :param dirs: 待切换的目的地目录
        :return:
        '''
        if dirs in os.listdir(self.current_dir):
            self.current_dir = os.path.join(self.current_dir,dirs)
            self.conn.send(b'200')

        elif '..' == dirs:
            # 将路径通过操作系统路劲分隔符分裂成列表并删除最后一个
            list_path = self.current_dir.split(os.sep)
            base_path = self.path.split(os.sep)
            list_path.pop(-1)
            if len(list_path) >= len(base_path): # 当该路径列表参数大于等于默认用户的根目录个数时
                # 重组路径
                new_path = str(os.sep).join(list_path)
                self.current_dir = new_path
                self.conn.send(b'200')
            else:                               # 当该路径列表参数已经小于默认根目录时
                self.current_dir = self.path
                self.conn.send(b'200')
        else:
            self.conn.send(b'202')

    def get(self,filename):
        '''
        用户获取文件，服务端传送文件
        :param filename: 文件名
        :return:
        '''
        count_size = self.count_size(self.path)
        quoto = self.user[list(self.user.keys())[0]]['quota']
        if count_size >= quoto:
            self.conn.send(b'503')   # 空间已满
            self.logobj.error('user %s disk if full'%list(self.user.keys())[0])
        else:
            if filename in os.listdir(self.current_dir) and \
                    os.path.isfile(os.path.join(self.current_dir,filename)):     # 检测服务器上是否有此文件
                md5 = hashlib.md5()
                md5.update(bytes(filename,'utf-8'))
                head = {}
                head['md5'] = md5.hexdigest()
                head['data-size'] = os.path.getsize(os.path.join(self.current_dir,filename))
                head_bytes = bytes(json.dumps(head),'utf8')
                self.conn.send(struct.pack('i',len(head_bytes)))
                self.conn.send(head_bytes)
                f = open(os.path.join(self.current_dir,filename),'rb')
                for lines in f:
                    self.conn.send(lines)
                f.close()
                self.logobj.info('send file to client %s'%str(self.addr))
            else:
                self.conn.send(b'501')  # 不存在此文件
                self.logobj.error('not found the file')

    def re_get(self,file):
        '''
        断点续传
        :return:
        '''

        recevied_size = file[0] # 已接收大小
        total_size = file[1]    # 总大小
        file_md5 = file[2]           # md5
        filename = file[-1]     # 文件名
        filename = filename.replace('.download','')
        # 搜索文件所在位置
        file_pth = self.search_file(filename,total_size,self.path)
        if file_pth:
            # 重新打包
            md5 = hashlib.md5()
            md5.update(bytes(filename,'utf-8'))
            head = {}
            head['md5'] = md5.hexdigest()
            head['data-size'] = os.path.getsize(file_pth)
            head_bytes = bytes(json.dumps(head),'utf8')
            self.conn.send(struct.pack('i',len(head_bytes)))
            self.conn.send(head_bytes)

            # 发送
            f = open(file_pth,'rb')
            for lines in f:
                self.conn.send(lines)
            else:
                f.close()
                self.logobj.info('send file to client %s'%str(self.addr))
        else:
            self.conn.send(b'501')  # 不存在此文件
            self.logobj.error('not found the file')

    def search_file(self,filename,total_size,path):
        '''
        搜索文件
        :param filename: 文件名
        :param path: 路径
        :return: 返回搜到的文件路径+文件名
        '''
        for i in os.listdir(path):
            temp_path = os.path.join(path,i)
            if os.path.isfile(temp_path):
                if i == filename:
                    if os.path.getsize(temp_path) == total_size:
                        print('got it')
                        return temp_path
            else:
                self.search_file(filename,temp_path)


    def dir(self):
        '''
        查看当前目录
        :return:
        '''
        cmd = 'dir %s'%self.current_dir
        if os.name == 'nt':
            cmd = cmd.replace('/','\\')
        obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        msg = obj.stderr.read()
        if not msg:
            msg = obj.stdout.read()

        # 打包数据并发送
        head = {}
        head['data-size'] = len(msg)
        head_bytes = bytes(json.dumps(head),'utf8')
        head_bytes_len = struct.pack('i',len(head_bytes))
        self.conn.send(head_bytes_len)
        self.conn.send(head_bytes)
        self.conn.send(msg)

    def put(self,filename):
        '''
        用户上传文件，服务端接收文件
        :param filename: 文件名
        :return:
        '''
        count_size = self.count_size(self.path)
        quoto = self.user[list(self.user.keys())[0]]['quota']
        if count_size >= quoto:
            self.conn.send(b'503')   # 空间已满
            self.logobj.error('user %s disk if full'%list(self.user.keys())[0])
        else:
            if filename in os.listdir(self.current_dir):   # 检测服务器上是否已有同名文件
                self.conn.send(b'502')
            else:
                struct_head_len = self.conn.recv(4)
                head_len = struct.unpack('i',struct_head_len)[0]
                msg_dict = eval(self.conn.recv(head_len).decode('utf-8'))
                msg_md5 = msg_dict['md5']
                msg_size = msg_dict['data-size']
                md5 = hashlib.md5()
                md5.update(bytes(filename,'utf8'))
                cont = b''
                while len(cont) < msg_size:
                    line = self.conn.recv(1024)
                    cont += line
                if md5.hexdigest() == msg_md5:
                    f = open(os.path.join(self.current_dir,filename),'wb')
                    f.write(cont)
                    f.close()
                    self.conn.send(b'200')  # 操作成功
                    self.logobj.info('recv file from client %s'%str(self.addr))
                else:
                    self.conn.send(b'402')  # MD5值改变

    def parser(self,res):
        '''
        解析用户传入的数据
        :param res: 传入的数据
        :return:
        '''
        res = json.loads(res)
        types = res['type']
        data = res.get('data')
        if data:        # 如果有数据则是登录或者get,put，cd等命令
            if hasattr(self,types):
                func = getattr(self,types)
                func(data)
        else:
            if hasattr(self,types):
                func = getattr(self,types)
                func()


    def auth(self,res):
        '''
        验证数据正确性
        :return:
        '''
        username = res['username']
        password = res['password']
        data = {}
        usersdata = load_dump_data.load_data()
        if username in usersdata and password == usersdata[username]['password']:
            data[username] = usersdata[username]  #组成新的键值对
            self.user = data
            self.path = os.path.join(self.base_path,self.user[username]['home'])
            self.current_dir = self.path
            os.chdir(self.path)
            self.conn.send(b'100')  # 登录成功
            self.logobj.info('client  %s connect and user %s logined'%(str(self.addr),username))
        else:
            self.conn.send(b'101')  # 登录失败
    def run_away(self):
        '''
        运行函数
        :return:
        '''
        self.server = self.create_ftp_sever()
        print('start...')
        while True:
            self.conn,self.addr = self.server.accept()
            # 这里由于addr是个元组，格式化输出有时会解析所，所以直接转为字符串
            print('客户端 %s 已上线...'%str(self.addr))
            self.logobj.info('client %s connection...'%str(self.addr))
            try:
                self.run()
            except Exception as e:
                print(e)
                self.conn.close()

    def run(self):
        while True:
            bytes_res = self.conn.recv(1024)
            if not bytes_res:
                del self.conn
                del self.addr
                print('客户端 %s 已下线...'%str(self.addr))
                break
            res = bytes_res.decode('utf-8')
            self.parser(res)

def server():
    '''
    ftp 服务器运行函数
    :return:
    '''
    server = ftp_server('tcp')
    server.run_away()