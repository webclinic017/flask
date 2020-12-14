#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/11/11 16:45
# @Site    :
# @File    : thread_pool.py
# @Software: PyCharm
"""
import queue
from concurrent.futures.thread import ThreadPoolExecutor


class BoundedThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers,thread_name_prefix)
        self._work_queue = queue.Queue(self._max_workers * 2)

