#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/4 16:04
@Author : zhaiyanming
"""


class MyBaseFailure(Exception):
    pass


class JsonpathExtractionFailed(MyBaseFailure):
    pass


class NotFoundError(MyBaseFailure):
    pass


class FileNotFound(FileNotFoundError,NotFoundError):
    pass


class SqlNotFound(NotFoundError):
    pass

class AssertTypeError(MyBaseFailure):
    pass


class DataAcquisitionFailed(MyBaseFailure):
    pass


class ValueTypeError(MyBaseFailure):
    pass


class SendMessageError(MyBaseFailure):
    pass


class ValueNotFoundError(MyBaseFailure):
    pass
