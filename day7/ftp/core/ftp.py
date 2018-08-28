#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from lib import login_auth
from lib import ftp_client

@login_auth.login
def main(arg=None):         # arg只是作为一个位置参数占位
    ftp_client.client(arg)  # 登录认证成功后，此时的arg已经变成用户的数据信息了
    return arg              # 返回用户数据

if __name__ == '__main__':
    main()