#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/6/26 11:48
# @Site    :
# @File    : error_code.py
# @Software: PyCharm
"""
from utils.errors.base_errors.error import APIException


class Success(APIException):
    """
    返回成功数据
    """

    code = 201
    returncode = 201
    message = "成功"
    result = ""


class DeleteSuccess(Success):
    code = 202


class ServerError(APIException):
    """定义python中最原始的错误"""

    code = 500
    returncode = 500
    message = "服务器未响应"
    result = ""

class ClientTypeEnumError(APIException):

    code = 422
    returncode = 422
    message = "请求参数，语义错误"
    result = ""


class ClientTypeError(APIException):
    # 400 请求参数错误
    # 401 未授权
    # 403 禁止访问
    # 404 没有找到页面
    # 500 服务器产生未知错误
    # 200 查询成功
    # 201 创建或更新成功
    # 204 删除成功
    # 301/302 重定向
    code = 400
    returncode = 400
    message = "非法请求"
    result = ""


class NotFound(APIException):
    code = 404
    returncode = 404
    message = "找不到资源"
    result = ""


class AuthFailed(APIException):
    """授权失败"""

    code = 401
    returncode = 401
    message = "授权失败"
    result = ""


class Forbidden(APIException):
    """禁止访问，权限禁止"""

    code = 403
    returncode = 403
    message = "禁止访问"
    result = ""
