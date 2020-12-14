#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:36
# @Site    :
# @File    : base.py
# @Software: PyCharm
"""

import time
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, DateTime, SmallInteger, func
from contextlib import contextmanager

from utils.errors.error_codes.error_code import NotFound
from utils.errors.response_code_msg.response_code_msg import ResponseMessage

from flask_apscheduler import APScheduler
scheduler = APScheduler()

logger = logging.getLogger(__name__)

class SQLAlchemy(_SQLAlchemy):
    """
    创建一个上下文管理器
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            raise e


class Query(BaseQuery):
    """
    覆盖查询类 重写filter_by方法
    """

    def filter_by(self, **kwargs):
        if "status" not in kwargs.keys():
            kwargs["status"] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        # 判断是否存在
        rv = self.first()
        if not rv:
            logger.error(ResponseMessage.NoUserErr)
            raise NotFound(message=ResponseMessage.NoResourceFound)
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    """
    模型的基类，为所有模型添加create_time,status属性
    为方便好用
    """

    __abstract__ = True
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='修改时间')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = datetime.now()
    @property
    def create_datetime_stamp(self):
        """
        转时间戳
        :return:
        """
        if self.create_time:
            return int(time.mktime(self.create_time.timetuple()))
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def __getitem__(self, item):
        return getattr(self, item)
