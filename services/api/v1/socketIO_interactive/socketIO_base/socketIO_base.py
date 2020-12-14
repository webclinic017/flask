#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 17:05
# @Site    :
# @File    : socketIO_base.py
# @Software: PyCharm
"""

import logging
from flask import request, current_app

from utils.socket_utils.socket_utils import SocketView, SocketRedis
from utils.day_zero_time.day_zero_time import get_day_zero_time

logger = logging.getLogger(__name__)


class BaseSocketDataView(SocketView):
    method_decorators = []
    def CONNECT(self, *args):
        print("连接sid:", request.sid)
        current_app.redis.incr("all_visit_count")
        now, expire_time = get_day_zero_time()
        current_app.redis.incr(f"{now}_visit_count")
        current_app.redis.expire(f"{now}_visit_count", expire_time)

    def DISCONNECT(self):
        # 用户map注销
        SocketRedis.delete()
        # 在线用户注销
        current_app.redis.srem(self.onlineRedisKey("user_auth_online"), request.sid)



base_socket_obj = BaseSocketDataView()
