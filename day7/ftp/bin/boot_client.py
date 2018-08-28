#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from lib import ftp_client

def run_client():
    ftp_client.client()

if __name__ == '__main__':
    run_client()