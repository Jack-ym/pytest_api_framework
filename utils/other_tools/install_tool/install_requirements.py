#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/7 16:36
@Author : zhaiyanming
"""
"""判断程序是否每次会更新依赖库，如有更新，则自动安装"""
import os
import chardet
from common.setting import ensure_path_sep
from utils.logging_tool.log_control import INFO
from utils import config

os.system("pip3 install chardet")


class InstallRequirements:
    """
    自动识别安装最新的依赖库
    """

    def __init__(self):
        self.version_library_comparisons_path = ensure_path_sep('/utils/other_tools/install_tool/') \
                                                + 'version_library_comparisons.txt'
        self.requirements_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
                                 + os.sep + 'requirements.txt'
        self.mirror_url = config.mirror_source

    def read_version_library_comparisons_txt(self):
        """
        获取版本比对默认的文件
        :return:
        """
        with open(self.version_library_comparisons_path, 'r', encoding='utf-8') as file:
            return file.read().strip(' ')

    @classmethod
    def check_charset(cls, file_path):
        """获取文件的字符集"""
        with open(file_path, 'rb') as file:
            data = file.read(4)
            charset = chardet.detect(data)['encoding']
        return chardet

    def read_requirements(self):
        """
        获取安装文件
        :return:
        """
        file_data = ""
        with open(self.requirements_path,
                  'r',
                  encoding=self.check_charset(self.requirements_path)
                  ) as file:
            for line in file:
                if "[0m" in line:
                    line = line.replace("[0m", "")
                file_data += line
        with open(
                self.requirements_path,
                "w",
                encoding=self.check_charset(self.requirements_path)
        ) as file:
            file.write(file_data)
        return file_data

    def text_comparison(self):
        """版本库比对"""
        read_version_library_comparison_txt = self.read_version_library_comparisons_txt()
        read_requirements = self.read_requirements()
        if read_version_library_comparison_txt == read_requirements:
            INFO.logger.info("程序中未检查到更新版本库，已为您跳过自动安装库")
        # 程序中发现新版本，则安装
        else:
            INFO.logger.info("程序中监测到您更新了依赖库，已为您自动安装")
            os.system(f"pip3 install -r {self.requirements_path}")
            with open(self.version_library_comparisons_path, "w",
                      encoding=self.check_charset(self.requirements_path)) as file:
                file.write(read_requirements)


if __name__ == '__main__':
    InstallRequirements().text_comparison()
