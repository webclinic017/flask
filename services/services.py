#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:17
# @Site    :
# @File    : services.py
# @Software: PyCharm
"""
import uuid
from decimal import Decimal
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from sqlalchemy_utils import Choice
from utils.errors.error_codes.error_code import ServerError
import datetime

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            # print(dict(o))
            return dict(o)
        if isinstance(o, datetime.datetime):
            # 格式化时间
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, Decimal):
            return "%.2f" % o
        if isinstance(o, Choice):
            return o.value
        if isinstance(o, uuid.UUID):
            # 格式化uuid
            return str(o)
        if isinstance(o, bytes):
            # 格式化字节数据
            return o.decode("utf-8")
        raise ServerError()

class Flask(_Flask):
    json_encoder = JSONEncoder
