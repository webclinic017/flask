#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 17:28
# @Site    :
# @File    : user_count.py
# @Software: PyCharm
"""
from models.account_models import User
from services.api.v1.base_http.base_http import Service


class UserCountView(Service):
    __model__ = User
    __methods__ = ["GET", "DELETE", "POST", "PUT"]
    service_name = 'user_count_view'
    decorators = []
