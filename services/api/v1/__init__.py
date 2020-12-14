#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:50
# @Site    :
# @File    : __init__.py
# @Software: PyCharm
"""
from flask import Blueprint

from services.api.v1.user_count.user_count import UserCountView


def create_blueprint_v1():
    bp_v1 = Blueprint("v1", __name__)
    bp_v1.add_url_rule(
        "/UserCount/",
        defaults={"key": None},
        endpoint="user_count_view1",
        view_func=UserCountView.as_view("user_count_view1"),
        methods=["GET", "POST"],
    )
    bp_v1.add_url_rule(
        "/UserCount/<string:key>/",
        endpoint="user_count_view2",
        view_func=UserCountView.as_view("user_count_view2"),
        methods=["GET", "DELETE", "PUT"],
    )
    return bp_v1
