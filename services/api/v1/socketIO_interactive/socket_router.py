#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 17:08
# @Site    :
# @File    : socket_router.py
# @Software: PyCharm
"""
from services.api.v1.extensions.extensions import socketio
from services.api.v1.socketIO_interactive.socketIO_base.socketIO_base import base_socket_obj

# 连接
socketio.on_event('connect', base_socket_obj.CONNECT)
# 断开
socketio.on_event("disconnect", base_socket_obj.DISCONNECT)

