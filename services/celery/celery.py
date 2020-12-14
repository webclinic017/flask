#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:39
# @Site    :
# @File    : celery.py
# @Software: PyCharm
"""

from celery import Celery

celery_app = Celery(__name__)

from services.task.async_task.demo import *
