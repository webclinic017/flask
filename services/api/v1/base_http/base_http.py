#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/12/13 16:58
# @Site    :
# @File    : base_http.py
# @Software: PyCharm
"""
import logging
from flask import request, current_app
from flask.views import MethodView
from sqlalchemy import inspect

from models.base.base import db
from utils.base_response.response import ResponseMsg
from utils.errors.response_code_msg.response_code_msg import ResponseCode, ResponseMessage


logger = logging.getLogger(__name__)


class BaseQuery(object):
    """
    search function
    """
    __model__ = None
    def _find(self, args):
        return self.__model__.query.filter_by(*args).all()

    def _calculation_institution_user(self,data):
        """
        机构人员统计处理
        :param data:
        :return:
        """

        return data

    def _find_by_page(self, pageNum, pageSize, query, by):
        base = self.__model__.query.filter(*query).order_by(*by)
        cnt = base.count()
        data = base.slice(pageNum * pageSize, (pageNum + 1) * pageSize).all()
        return cnt, data
    def _get(self, key):
        return self.__model__.query.filter_by(id=key).first_or_404()

    def _create(self, args):
        for base in args:
            # md = self.__model__()()
            md = self.__model__()
            for k, v in base.items():
                # if k in search_key_list:
                setattr(md, k, v)
            db.session.add(md)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False
    def _update(self, key, kwargs):
        model = self._get(key)
        if model:
            for k, v in kwargs.items():
                setattr(model, k, v)
            try:
                db.session.add(model)
                db.session.commit()
                return True
            except Exception as e:
                logger.error(e)
                return False
        else:
            return False

    def _delete(self, key):
        model = self._get(key)
        if model:
            try:
                # 软删除
                with db.auto_commit():
                    model.delete()
                return True
            except:
                return False
        else:
            return False
    def parse_data(self, data):
        try:
            search_key_list = self.__model__().keys()
        except:
            search_key_list = []
        if data:
            if isinstance(data, (list, tuple)):
                if not search_key_list:
                    data = list(map(lambda x: {p.key: getattr(x, p.key)
                                               for p in self.__model__.__mapper__.iterate_properties
                                               }, data))
                # 根据keys定义查询多信息
                else:
                    data = list(map(lambda x: {p.key: getattr(x, p.key)
                                               for p in self.__model__.__mapper__.iterate_properties if p.key in search_key_list
                                               }, data))

            else:
                if not search_key_list:
                    data = {p.key: getattr(data, p.key)
                            for p in self.__model__.__mapper__.iterate_properties}
                else:
                    data = {p.key: getattr(data, p.key)
                            for p in self.__model__.__mapper__.iterate_properties if p.key in search_key_list}

        return data


class BaseParse(object):
    """
    识别查询字段
    """
    __model__ = None
    __request__ = request
    by = frozenset(['by'])
    query = frozenset(['gt', 'ge', 'lt', 'le', 'ne', 'eq', 'ic', 'ni', 'in'])
    def __init__(self):
        self._operator_funcs = {
            'gt': self.__gt_model,# 大于
            'ge': self.__ge_model,# 大于等于
            'lt': self.__lt_model,# 小于
            'le': self.__le_model,# 小于等于
            'ne': self.__ne_model,# 不等于
            'eq': self.__eq_model,# 等于
            'ic': self.__ic_model,# 包含
            'ni': self.__ni_model,# 不包含
            'by': self.__by_model,# 排序
            'in': self.__in_model,# 查询多个相同字段的值
        }
    def _parse_pageNum_pageSize(self):
        """
        获取页码和获取每页数据量
        :return:
             pageNum 页码
             pageSize 每页数据量
        """
        default_pageNum = current_app.config["PAGE_NUM"]
        default_pageSize = current_app.config["PAGE_SIZE"]
        pageNum = self.__request__.args.get("pageNum", default_pageNum)
        pageSize = self.__request__.args.get("pageSize", default_pageSize)
        pageNum = int(pageNum) - 1
        pageSize = int(pageSize)
        return pageNum, pageSize

    def _args_expansion(self,args):
        """
        查询扩充
        :param args:
        :return:
        """
        args = dict(args)
        return args

    def _parse_query_field(self):
        """
        解析查询字段
        :return: query_field 查询字段
                 by_field 排序字段
        """
        args_data = self.__request__.args
        args = self._args_expansion(args_data)
        # 添加status,只查询激活状态
        # args = dict(args)
        # args["eq-status"] = 1
        query_field = list()
        by_field = list()
        for query_key, query_value in args.items():
            if not query_value:
                continue
            split_query_key = query_key.split("-", 1)
            if len(split_query_key) != 2:
                continue
            operator, key = split_query_key
            if not self._check_key(key=key):
                continue
            if operator in self.query:
                data = self._operator_funcs[operator](key=key, value=query_value)
                query_field.append(data)
            elif operator in self.by:
                data = self._operator_funcs[operator](key=key, value=query_value)
                by_field.append(data)
        return query_field, by_field
    def _parse_create_field(self):
        """
        检查字段是否为model的字段,并过滤无关字段.
        1.list(dict) => list(dict)
        2. dict => list(dict)
        :return:
        """
        obj = self.__request__.get_json(force=True)
        if isinstance(obj, list):
            create_field = list()
            for item in obj:
                if isinstance(item, dict):
                    base_dict = self._parse_field(obj=item)
                    create_field.append(base_dict)
            return create_field
        elif isinstance(obj, dict):
            return [self._parse_field(obj=obj)]
        else:
            return list()
    def _parse_field(self, obj=None):
        """
        检查字段模型中是否有，并删除主键值
        :param obj:
        :return:
        """
        obj = obj if obj is not None else self.__request__.get_json(force=True)
        field = dict()
        # 获取model主键字段
        primary_key = map(lambda x: x.name, inspect(self.__model__).primary_key)

        for key, value in obj.items():
            if key in primary_key:
                continue
            if self._check_key(key):
                field[key] = value
        return field

    def _check_key(self, key):
        """
        检查model是否存在key
        :param key:
        :return:
        """
        if hasattr(self.__model__, key):
            return True
        else:
            return False

    def __gt_model(self, key, value):
        """
        大于
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key) > value


    def __ge_model(self, key, value):
        """
        大于等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key) > value

    def __lt_model(self, key, value):
        """
        小于
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key) < value

    def __le_model(self, key, value):
        """
        小于等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key) <= value

    def __eq_model(self, key, value):
        """
        等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key) == value

    def __ne_model(self, key, value):
        """
        不等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key) != value

    def __ic_model(self, key, value):
        """
        包含
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key).like('%{}%'.format(value))

    def __ni_model(self, key, value):
        """
        不包含
        :param key:
        :param value:
        :return:
        """
        return getattr(self.__model__, key).notlike('%{}%'.format(value))

    def __by_model(self, key, value):
        """
        :param key:
        :param value: 0:正序,1:倒序
        :return:
        """
        try:
            value = int(value)
        except ValueError as e:
            return getattr(self.__model__, key).asc()
        else:
            if value == 1:
                return getattr(self.__model__, key).asc()
            elif value == 0:
                return getattr(self.__model__, key).desc()
            else:
                return getattr(self.__model__, key).asc()

    def __in_model(self, key, value):
        """
        查询多个相同字段的值
        :param key:
        :param value:
        :return:
        """
        value = value.split(',')
        return getattr(self.__model__, key).in_(value)



class Service(BaseParse, BaseQuery, MethodView):
    __model__ = None
    # decorators = [view_route]
    def get(self, key=None):
        """
        获取列表或单条数据
        :param key:
        :return:
        """
        res = ResponseMsg()
        if key is not None:
            data = self.parse_data(self._get(key=key))
            if data:
                res.update(result=data)
            else:
                res.update(returncode=ResponseCode.NoResourceFound, message=ResponseMessage.NoResourceFound)# 未找到资源
        else:
            query, by = self._parse_query_field()
            # print("多用户条件查询",query)
            pageNum, pageSize = self._parse_pageNum_pageSize()
            cnt, data = self._find_by_page(pageNum=pageNum, pageSize=pageSize, query=query, by=by)
            data = self.parse_data(data)
            if data:
                data = self._calculation_institution_user(data)
                res.update(result=data)
            else:
                res.update(returncode=ResponseCode.NoResourceFound, message=ResponseMessage.NoResourceFound)# 未找到资源
            res.add_field(name='total', value=cnt)
            res.add_field(name='pageNum', value=pageNum + 1)
            res.add_field(name='pageSize', value=pageSize)
            res.update(result=data)
        return res.data

    def post(self):
        """
        创建数据
        1.单条
        2.多条
        :return:
        """
        res = ResponseMsg()
        # print("request:===>post")
        data = self._parse_create_field()
        if data:
            if not self._create(args=data):
                res.update(returncode=ResponseCode.Fail)#失败
        else:
            res.update(returncode=ResponseCode.Fail)#失败
        return res.data



    def put(self, key=None):
        """
        更新某个数据
        :return:
        """
        # 表单验证通过:
        res = ResponseMsg()
        if key is None:
            # 500失败
            res.update(returncode=ResponseCode.Fail, message= ResponseMessage.Fail)
        else:
            data = self._parse_field()
            print("解析后结果",data)

            # 更改数据
            if not self._update(key=key, kwargs=data):
                # 500失败
                res.update(returncode=ResponseCode.Fail, message= ResponseMessage.Fail)
        return res.data


    def delete(self, key=None):
        """
        删除某个数据
        :return:
        """
        res = ResponseMsg()
        if key is None:
            # 无效参数
            res.update(returncode=ResponseCode.InvalidParameter, message= ResponseMessage.InvalidParameter)
        elif not self._delete(key=key):
            # 失败
            res.update(returncode=ResponseCode.Fail, message= ResponseMessage.Fail)
        return res.data
