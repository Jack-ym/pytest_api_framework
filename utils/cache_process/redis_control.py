#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/4 16:03
@Author : zhaiyanming
"""
"""redis缓存封装"""

from typing import Text, Any
import redis


class RedisHandler:
    """redis缓存读取封装"""

    def __init__(self):
        self.host = '127.0.0.0'
        self.port = 6379
        self.database = 0
        self.password = 123456
        self.charset = 'UTF-8'
        self.redis = redis.Redis(
            self.host,
            port=self.port,
            password=self.password,
            decode_responses=True,
            db=self.database
        )

    def set_string(self, name: Text,
                   value, exp_time=None,
                   exp_milliseconds=None,
                   name_not_exist=False,
                   name_exist=False) -> None:
        """
        缓存中写入单个str
        :param name: 缓存名称
        :param value: 缓存值
        :param exp_time: 过期时间（秒）
        :param exp_milliseconds: 过期时间（毫秒）
        :param name_not_exist: 如果设置为True，则只有name不存在时，当前set操作才执行（新增）
        :param name_exist: 如果设置为True，则只有name存在时，当前set操作才执行（修改）
        :return:
        """
        self.redis.set(
            name,
            value,
            ex=exp_time,
            px=exp_milliseconds,
            nx=name_not_exist,
            xx=name_exist
        )

    def key_exist(self, key: Text):
        """判断redis中的key是否存在"""
        return self.redis.exists(key)

    def incr(self, key: Text):
        """
        使用incr方法处理并发问题
        当key不存在时，则会先初始化为0，每次调用则会+1
        :param key:
        :return:
        """
        self.redis.incr(key)

    def get_key(self, name: Any) -> Text:
        """读取缓存"""
        return self.redis.get(name)

    def set_many(self, *args, **kwargs):
        """
        批量设置
        支持如下方式批量设置缓存
        eg: set_many({'k1':'v1','k2':'v2'})
            set_many(k1='v1',k2='v2')
        :param args:
        :param kwargs:
        :return:
        """
        self.redis.mset(*args, **kwargs)

    def get_many(self, *args):
        """获取多个值"""
        results = self.redis.mget(*args)
        return results

    def del_all_cache(self):
        """清理所有的数据"""
        for key in self.redis.keys():
            self.del_cache(key)

    def del_cache(self, name):
        """删除缓存"""
        self.redis.delete(name)
