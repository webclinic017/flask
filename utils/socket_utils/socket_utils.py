#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/10/31 13:27
# @Site    :
# @File    : socket_utils.py
# @Software: PyCharm
"""
import json

import six
from collections import Mapping

from flask import current_app, request

from utils.day_zero_time.day_zero_time import get_day_zero_time


class SocketViewMeta(type):
    """
    socketio 视图
    """

    @classmethod
    def options(cls, bases, attrs):
        deco = attrs.get("method_decorators")
        for key, value in attrs.items():
            if key.startswith("SOCKET_"):
                if isinstance(deco, Mapping):
                    decorators = deco.get(key, [])
                else:
                    decorators = deco
                for decorator in decorators:
                    value = decorator(value)
                attrs[key] = value
        return attrs

    def __new__(cls, name, bases, attrs):
        new_attrs = cls.options(bases, attrs)
        return super().__new__(cls, name, bases, new_attrs)

@six.add_metaclass(SocketViewMeta)
class SocketView(object):
    def onlineRedisKey(self, key):
        mapping = {
            "user_auth_online": "online_users",
        }
        return mapping[key]

    def imaconlineRedisKey(self, key):
        mapping = {
            "imac": "online_imac",
            "imac_bind": "online_bind_imac",
        }
        return mapping[key]


class SocketRedis(object):
    key = "socketMap"

    @classmethod
    def set(cls, user: str):
        """存储socket的映射"""
        current_app.redis.hset(cls.key, request.sid, user)

    @classmethod
    def get(cls):
        return current_app.redis.hget(cls.key, request.sid)

    @classmethod
    def delete(cls):
        return current_app.redis.hdel(cls.key, request.sid)

    @classmethod
    def get_one(cls, sid):
        return current_app.redis.hget(cls.key, sid)

    @classmethod
    def abrupt_disconnect(cls, sid):
        return current_app.redis.hdel(cls.key, sid)


class InstitutionSocketRedis(object):
    """
    机构在线用户：
    """

    @staticmethod
    def sadd(name):
        current_app.redis.sadd(name, request.sid)

    @staticmethod
    def srem(name):
        current_app.redis.srem(name, request.sid)

    @staticmethod
    def smembers(name):
        return current_app.redis.smembers(name)


class VrImacSocketRedis(object):  # 废弃
    """
    vr一体机手环注册
    """

    key = "VrSet"

    @classmethod
    def sadd(cls, value):
        return current_app.redis.sadd(cls.key, value)

    @classmethod
    def srem(cls, value):
        return current_app.redis.srem(cls.key, value)

    @classmethod
    def smembers(cls):
        return current_app.redis.smembers(cls.key)

    @classmethod
    def sismember(cls, value):
        """
        是否存在
        :param value:
        :return:
        """
        return current_app.redis.sismember(cls.key, value)


class SocketInitMapFingerData(object):
    """
    指压板初始化Map数据(待定)
    """

    key = "fingerHrvSocketMap"

    @classmethod
    def set(cls, data: str):
        """存储socket的映射"""
        current_app.redis.hset(cls.key, request.sid, data)

    @classmethod
    def get(cls):
        return current_app.redis.hget(cls.key, request.sid)

    @classmethod
    def delete(cls):
        return current_app.redis.hdel(cls.key, request.sid)

    @classmethod
    def get_one(cls, sid):
        return current_app.redis.hget(cls.key, sid)

    @classmethod
    def get_many(cls, sid_set):
        return current_app.redis.hmget(cls.key, list(sid_set))


class SocketMapOnceFingerData(object):
    """
    单次训练记录：
    """

    default_head = "once_finger:{}"

    @classmethod
    def exists(cls):
        name = cls.default_head.format(request.sid)
        return current_app.redis.exists(name)

    @classmethod
    def hmget(cls, lst: list):
        name = cls.default_head.format(request.sid)
        return current_app.redis.hmget(name, lst)

    @classmethod
    def hget(cls, data: str):
        name = cls.default_head.format(request.sid)
        current_app.redis.hget(name, data)

    @classmethod
    def hset(cls, key: str, value: str):
        name = cls.default_head.format(request.sid)
        return current_app.redis.hset(name, key, value)

    @classmethod
    def hmset(cls, kv: dict):
        name = cls.default_head.format(request.sid)
        current_app.redis.hmset(name, kv)

    @classmethod
    def hget_one(cls, sid: str):
        name = cls.default_head.format(sid)
        return current_app.redis.hget(name)

    @classmethod
    def hget_one_field(cls, sid: str, field: str):
        name = cls.default_head.format(sid)
        return current_app.redis.hget(name, field)

    @classmethod
    def hgetall(cls, sid: str):
        name = cls.default_head.format(sid)
        return current_app.redis.hgetall(name)

    @classmethod
    def hdel(cls):
        name = cls.default_head.format(request.sid)
        current_app.redis.delete(name)
