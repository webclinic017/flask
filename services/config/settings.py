#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:27
# @Site    :
# @File    : settings.py
# @Software: PyCharm
"""

import logging
import os

from collections import Mapping

import redis
import rsa
from utils.thread_pool.thread_pool import BoundedThreadPoolExecutor


class BaseConfig(object):
    @classmethod
    def init_app(cls, app):
        app.config.from_object(cls)
        app.redis = app.config.get('COMMON_REDIS', None)
        app.executor = app.config.get('COMMON_THREDA_POOL', None)


class Config(BaseConfig):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR,os.path.pardir))
    TOKEN_EXPIRATION = 60 * 60 * 2
    DEBUG = True
    LOG_LEVEL = logging.INFO
    # 字体文件
    FONT_PATH = os.path.join(PROJECT_DIR, 'font', 'simhei.ttf')
    # 日志:
    LOGGING_CONFIG_PATH = "./services/config/logging_conf.yaml"
    # 是否跨平台验证
    IS_CROSS = True
    # ENCRYPTION_PATH = r"./utils/encryption/pem"
    # # 密钥
    # with open(f"{ENCRYPTION_PATH}\pub_key.pem", 'r')as x:
    #     PUB_KEY = rsa.PublicKey.load_pkcs1(x.read().encode())
    PAGE_NUM = "1"
    PAGE_SIZE = "10"
    # JWT SIGN
    SIGN = "#KD(S@de!,.s"
    EXP = 5 * 60 * 60
    DELAY = 60 * 60 * 24 * 5
    # MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False# 调式启动，部署关闭
    SQLALCHEMY_ECHO = False# 调式启动，部署关闭
    SQLALCHEMY_POOL_RECYCLE = 3 * 60 * 60
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True# 连接结束后自定提交数据库中变动
    # AES
    VI = '0102030405060708'#密斯偏移量
    AES_KEY = "0CoJUm6Qyw8W8jud"
    # 线程池
    COMMON_THREDA_POOL = BoundedThreadPoolExecutor()
    # 指纹刷
    FINGER_EXP = 300


class DevelopConfig(Config):
    """开发环境下的配置"""
    VERSION = "v1"
    DEBUG = True
    # mysql
    DB_USERNAME = "root"
    DB_PASSWORD = "123"
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_NAME = "device_manage"
    DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
        DB_USERNAME,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    # redis
    DB_REDIS_PORT = 6379
    DB_REDIS_HOST = "127.0.0.1"
    DB_REDIS_DB = 1  # sso_db and current_data
    DB_REDIS_DB2 = 5  # permission_db
    REDIS_POOL = redis.ConnectionPool(host=DB_REDIS_HOST, port=DB_REDIS_PORT, db=DB_REDIS_DB, max_connections=10,
                                      decode_responses=True)
    COMMON_REDIS = redis.StrictRedis(connection_pool=REDIS_POOL)
    # celery
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_REDIS_DB = 2
    CELERY_REDIS_HOST = "127.0.0.1"
    CELERY_REDIS_PORT = "6379"

    CELERYD_TASK_SOFT_TIME_LIMIT = 200
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', ]
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
    JOBS = [
        {
            'id': 'calculate_to_db_uv',
            'func': 'services.task.time_task.pv_uv:calculate_to_db_uv',
            # 'args': (1, 2),
            'trigger': 'cron',
            'day_of_week': "0-6",
            'hour': 23,
            'minute': 40,
        },
        {
            'id': 'calculate_pv',
            'func': 'services.task.time_task.pv_uv:calculate_pv',
            'trigger': 'cron',
            'day_of_week': "0-6",
            'hour': 23,
            'minute': 40,
        },
    ]


class ProductConfig(Config):
    """生成环境下的配置"""
    VERSION = 'v1'
    DEBUG = False
    LOG_LEVEL = logging.WARNING

    # mysql
    DB_USERNAME = "root"
    DB_PASSWORD = "123"
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_NAME = "special_arm_db"
    DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
        DB_USERNAME,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    # redis
    DB_REDIS_PORT = 6379
    DB_REDIS_HOST = "127.0.0.1"
    DB_REDIS_DB = 1  # sso_db and current_data
    DB_REDIS_DB2 = 5  # permission_db
    REDIS_POOL = redis.ConnectionPool(host=DB_REDIS_HOST, port=DB_REDIS_PORT, db=DB_REDIS_DB, max_connections=10,
                                      decode_responses=True)
    COMMON_REDIS = redis.StrictRedis(connection_pool=REDIS_POOL)
    # celery
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_REDIS_DB = 2
    CELERY_REDIS_HOST = "127.0.0.1"
    CELERY_REDIS_PORT = "6379"
    SCHEDULER_OPEN = True  # 是否启动定时任务
    SCHEDULER_API_ENABLED = True
    CELERYD_TASK_SOFT_TIME_LIMIT = 200
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', ]
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
    JOBS = [
        {
            'id': 'calculate_to_db_uv',
            'func': 'services.task.time_task.pv_uv:calculate_to_db_uv',
            # 'args': (1, 2),
            'trigger': 'cron',
            'day_of_week': "0-6",
            'hour': 10,
            'minute': 42,
            # 'seconds': 20
        },
        {
            'id': 'calculate_pv',
            'func': 'services.task.time_task.pv_uv:calculate_pv',
            'trigger': 'interval',
            # 'hour': 12,
            # 'minute': 0,
            'seconds': 10
        },
    ]

    # 路由白名单
    WHITE_PATH = ["/v1/SuperAdminAuth/", "/v1/Auth/", "/v1/LoginOut/", "/v1/UserAuth/", "/v1/TrainType/",
                  "/v1/Register/User/"]
    # 路由免认证
    NO_PERMISSION = ["/v1/Avator/", "/v1/DrawHrvPNG/", "/v1/DrawHrvPNG/Show/"]




class TestConfig(Config):
    """测试环境下的配置"""

    DEBUG = True
    TESTING = True





envs = {
    "development": DevelopConfig,
    "production": ProductConfig,
    "testing": TestConfig,
}
