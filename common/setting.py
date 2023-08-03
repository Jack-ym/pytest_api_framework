#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/3 10:43
@Author : zhaiyanming
"""

import os
from typing import Text

def root_path():
    """
    获取项目根目录
    :return:
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path

def ensure_path_sep(path:Text)->Text:
    """
    兼容windows和linux不同环境系统路径
    :param path:
    :return:
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))
    elif "\\" in path:
        path = os.sep.join(path.split("\\"))
    return root_path() + path

if __name__ == '__main__':
    current_path = os.path.abspath(__file__)
    print(current_path)
    path_name = os.sep.join(current_path.split('/'))
    r = ensure_path_sep(current_path)
    print(r)
