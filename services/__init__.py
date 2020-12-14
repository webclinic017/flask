#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:17
# @Site    :
# @File    : __init__.py
# @Software: PyCharm
"""
import platform
import atexit
import yaml
import logging
from models.base.base import scheduler
from flask_compress import Compress
import logging.config
from services.config.settings import envs, Config
from .services import Flask
from flask_cors import CORS
from .celery.celery import celery_app
from .api.v1.extensions.extensions import socketio
from globals.bp_v1_manage import bp_v1
def register_blueprints(app):
    """
    蓝图注册
    :param app:
    :return:
    """
    version = app.config.get("VERSION")
    app.register_blueprint(bp_v1, url_prefix="/" + version)


def register_plugin(app):
    """
    数据库注册
    :param app:
    :return:
    """
    from models.base.base import db
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()



def scheduler_init(app):
    """
    保证系统只启动一次定时任务
    :param app:
    :return:
    """
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start()
            # app.logger.debug('Scheduler Started,---------------')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()
        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        # 上线更改........
        try:
            # msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,----------------')
        except Exception as e:
            print(e)
            print("发生错误2")
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)





def create_app(environ):
    app = Flask(__name__)
    config = envs.get(environ)
    assert config, (
        f'配置文件:{environ}不存在!,当前存在映射:{envs}'
    )
    # 配置
    config.init_app(app)
    # 日志注册
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)
    # 数据库
    register_plugin(app)
    # app注册
    register_blueprints(app)
    celery_conf = "redis://{}:{}/{}".format(app.config['CELERY_REDIS_HOST'], app.config['CELERY_REDIS_PORT'],
                                            app.config['CELERY_REDIS_DB'])
    celery_app.conf.update({"broker_url": celery_conf, "result_backend": celery_conf})
    celery_app.conf.ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': celery_conf,
            'default_timeout': 60 * 60
        }
    }
    if app.config.get("SCHEDULER_OPEN"):
        scheduler_init(app)
    socketio.init_app(app=app, async_mode="gevent", cors_allowed_origins='*')
    CORS(app, supports_credentials=True, resources=r'/*')
    # 数据压缩
    Compress(app)
    return app
