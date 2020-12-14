#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 17:22
# @Site    :
# @File    : user_auth.py
# @Software: PyCharm
"""
import logging

from models.account_models import User
from utils.base_response.response import ResponseMsg
from utils.redprint.redprint import Redprint

logger = logging.getLogger(__name__)
api = Redprint("UserAuth")


@api.route("/", methods=["POST"], endpoint="user_auth")
def user_auth():
    response = ResponseMsg()
    user = User.query.filter_by(account_name = "ming").first_or_404()

    return response.data
