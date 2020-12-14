#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:51
# @Site    :
# @File    : singles.py
# @Software: PyCharm
"""
from flask.signals import _signals

before_create = _signals.signal('before_create')


@before_create.connect
def bf(sender,*args,**kwargs):
    ...

