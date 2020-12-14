#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 17:17
# @Site    :
# @File    : account_models.py
# @Software: PyCharm
"""
from models.base.base import Base, db
from models.base.base_region import BaseRegionModel
from sqlalchemy import Column, Integer, String

class User(Base, BaseRegionModel):
    __tablename__ = "account_user"
    __table_args__ = (db.UniqueConstraint("account_name"),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_name = Column(String(32), comment="用户名")
    def keys(self):
        return [
            "id", "account_name", "status"
        ]
    def __str__(self):
        return "<User {}>".format(self.pid)
