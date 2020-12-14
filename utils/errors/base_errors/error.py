#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/6/26 11:43
# @Site    :
# @File    : error.py.py
# @Software: PyCharm
"""
import json
from flask import request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    """
    本身继承wekzeug的HTTPException
    要求返回错误信息格式：
    {
        "msg": "sorry, we make a mistake",
        "data": "",
        "request": "POST /v1/client/register"
    }
    """
    # 默认code
    code = 500
    returncode = 500
    message = "服务器未知错误."
    result = ""

    def __init__(self, message=None, returncode=None, code=None, result=None, headers=None):
        if code:
            self.code = code
        if returncode:
            self.returncode = returncode
        if result:
            self.result = result
        if message:
            self.message = message
        super(APIException, self).__init__(message, None)

    def get_body(self, environ=None):
        """
        封装json格式，将数据转为我们所需要格式
        :param environ:
        :return:
        """
        body = dict(
            message=self.message,
            returncode=self.returncode,
            result=self.result,
            request=request.method + " " + self.get_url_no_param(),
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """
        定义我们要返回数据类型为json
        :param environ:
        :return:
        """
        return [("Content-Type", "application/json")]

    @staticmethod
    def get_url_no_param():
        # url拼接
        full_path = str(request.full_path)
        main_path = full_path.split("?")
        return main_path[0]

