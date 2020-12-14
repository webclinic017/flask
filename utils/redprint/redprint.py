#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/6/26 22:48
# @Site    :
# @File    : redprint.py
# @Software: PyCharm
"""


class Redprint:
    """
    复写蓝图方法，用于注册函数
    """

    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = "/" + self.name
        for f, rule, options in self.mound:
            endpoint = self.name + "+" + options.pop("endpoint", f.__name__)
            # 添加路由
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
