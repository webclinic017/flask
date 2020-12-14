#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/10/31 13:40
# @Site    :
# @File    : day_zero_time.py
# @Software: PyCharm
"""
import datetime
import time

def get_day_zero_time() -> tuple:
    """
    获取到今日凌晨的秒数
    :return: 当前时间到今日凌晨所剩的秒数
    """
    now = datetime.datetime.now()
    date_zero = datetime.datetime.now().replace(year=now.year, month=now.month,
                                                day=now.day, hour=23, minute=59, second=59)
    date_zero_time = time.mktime(date_zero.timetuple())
    return now.strftime('%Y-%m-%d'), round(date_zero_time - time.time())
