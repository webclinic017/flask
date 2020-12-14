#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 17:16
# @Site    :
# @File    : base_region.py
# @Software: PyCharm
"""
from models.base.base import db
from sqlalchemy import Column, BIGINT


class BaseRegionModel(db.Model):
    __abstract__ = True
    province_id = Column(BIGINT, nullable=True, comment="省")
    city_id = Column(BIGINT, nullable=True, comment="市")
    county_id = Column(BIGINT, nullable=True, comment="区")
    town_id = Column(BIGINT, nullable=True, comment="街道")
    details_id = Column(BIGINT, nullable=True, comment="居委会")
