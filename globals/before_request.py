#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:49
# @Site    :
# @File    : before_request.py
# @Software: PyCharm
"""
from flask import request

from globals.bp_v1_manage import bp_v1


@bp_v1.before_app_request
def permission_filter():
    path = request.path
    return
