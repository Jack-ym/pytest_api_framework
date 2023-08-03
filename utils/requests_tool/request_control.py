#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/3 11:07
@Author : zhaiyanming
"""

class RequestControl:
    """
    封装请求
    """
    def __init__(self,yaml_case):
        self.__yaml_case = TestCase(**yaml_case)

    def file_data_exit(self,file_data)-> None:
        """判断上传文件时，data参数是否存在"""
        #兼容上传文件又要上传其他类型参数
            try:
                _data = self.__yaml_case.data
