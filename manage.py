#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 15:46
# @Site    :
# @File    : manage.py
# @Software: PyCharm
"""
from flask import make_response
from werkzeug.exceptions import HTTPException
from services import create_app, socketio, celery_app
from utils.base_response.response import ResponseMsg
from utils.base_response.response_message import ResponseMessage, ResponseCode
from utils.errors.base_errors.error import APIException
from utils.errors.error_codes.error_code import ServerError
from models.base.base import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
app = create_app("development")
manage = Manager(app)
Migrate(app, db)
manage.add_command("db", MigrateCommand)

@app.errorhandler(Exception)
def framework_err(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        message = e.description
        result = ""
        return APIException(message=message, returncode=code, code=code, result=result)
    else:
        if not app.config["DEBUG"]:
            return ServerError
        else:
            raise APIException(message=str(e), returncode=500, code=500, result="")




@app.errorhandler(401)
def error_401(error):
    """
    这个handler可以catch住所有abort(401)以及找不到对应router的处理请求
    :param error:
    :return:
    """
    err_description = error.__dict__.get("description")
    exist_token = err_description.get("flush_token")
    if exist_token:
        response = ResponseMsg(message=ResponseMessage.TokenFlush, returncode=ResponseCode.AuthFailed, result={"token": exist_token})
        return response.data, 401



@app.after_request
def af_request(resp):
    resp = make_response(resp)
    print(resp)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    return resp


if __name__ == '__main__':
    socketio.run(app=app, host="0.0.0.0", port=9999, debug=True)
    # manage.run()
