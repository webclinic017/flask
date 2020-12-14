#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:40
# @Site    :
# @File    : demo.py
# @Software: PyCharm
"""

from services.celery.celery import celery_app


@celery_app.task
def add_demo(x, y):
    return x + y

