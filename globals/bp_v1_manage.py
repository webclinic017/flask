#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:49
# @Site    :
# @File    : bp_v1_manage.py
# @Software: PyCharm
"""

from services.api.v1 import create_blueprint_v1

bp_v1 = create_blueprint_v1()

from .singles import *


