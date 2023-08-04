#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/4 11:28
@Author : zhaiyanming
"""
import logging
import colorlog

# 创建Logger对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建Handler对象，并设置日志级别
handler = colorlog.StreamHandler()
handler.setLevel(logging.DEBUG)

# 创建Formatter对象，并设置格式
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s %(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# 将Formatter对象添加到Handler对象
handler.setFormatter(formatter)

# 将Handler对象添加到Logger对象
logger.addHandler(handler)

# 输出不同级别的日志
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')

