#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2023/8/4 11:04
@Author : zhaiyanming
"""
import re
import datetime
import random
from datetime import date, timedelta, datetime
from jsonpath import jsonpath
from faker import Faker
from utils.logging_tool.log_control import ERROR


class Context:
    """正则替换"""

    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def random_int(cls) -> int:
        """随机数"""
        _data = random.randint(0, 5000)
        return _data

    def get_phone(self) -> int:
        """随机手机号码"""
        phone = self.faker.phone_number()
        return phone

    def get_id_number(self) -> int:
        """随机生成身份证号码"""
        id_number = self.faker.ssn()
        return id_number

    def get_female_name(self) -> str:
        """随机生成女生姓名"""
        female_name = self.faker.name_female()
        return female_name

    def get_name_name(self) -> str:
        """随机生成男生姓名"""
        male_name = self.faker.name_male()
        return male_name

    def get_email(self) -> str:
        """随机生成邮箱"""
        email = self.faker.email()
        return email

    @classmethod
    def get_time(cls) -> str:
        """计算当前时间"""
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    @classmethod
    def today_date(cls):
        """获取今日0点整时间"""
        _today = date.today().strftime("%Y-%m-%d") + "00:00:00"
        return str(_today)

    @classmethod
    def host(cls) -> str:
        from utils import config
        """获取接口域名 """
        return config.host

    @classmethod
    def app_host(cls) -> str:
        from utils import config
        """获取app接口域名 """
        return config.app_host


def sql_json(js_path, res):
    """提取sql中的json数据"""
    _json_data = jsonpath(res, js_path)[0]
    if _json_data is False:
        raise ValueError(f"sql中的jsonpath获取失败{res},{js_path}")
    return jsonpath(res, js_path)[0]


def sql_regular(value, res=None):
    """
    处理sql中的依赖数据，通过获取接口响应的jsonpath值进行替换
    :param value: jsonpath使用的返回结果
    :param res:
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)
    for i in sql_json_list:
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        key = str(sql_json(i, res))
        value = re.sub(pattern, key, value, count=1)
    return value


def cache_regular(value):
    from utils.cache_process.cache_control import CacheHandler
    """
    通过正则的方式读取缓存中的内容
    eg:
        $cache{login_init}
    """
    # 正则获取$cache{login_init}的值-->login_init
    regular_datas = re.findall(r"\$cache\{(.*?)\}", value)
    # 拿到的是一个list，循环数据
    for regular_data in regular_datas:
        value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        if any(i in regular_data for i in value_types) is True:
            value_types = regular_data.split(":")[0]
            regular_data = regular_data.split(":")[1]
            pattern = re.compile(r'\'\$cache\{' + value_types.split(":")[0] + ":" + regular_data + r'\}\'')
        else:
            pattern = re.compile(
                r'\$cache\{' + regular_data.replace('$', "\$").replace('[', '\[') + r'\}'
            )
        try:
            cache_data = CacheHandler.get_cache(regular_data)
            # 使用 sub方法，替换已经拿到的内容
            value = re.sub(pattern, str(cache_data), value)
        except Exception:
            pass
    return value


def regular(target):
    """使用正则替换请求数据"""
    try:
        regular_pattern = r'\${{(.*?)}}'
        while re.findall(regular_pattern,target):
            key = re.search(regular_pattern,target).group(1)
            value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
            if any(i in key for i in value_types)is True:
                func_name = key.split(":")[1].split("(")[0]
                value_name = key.split(":")[1].split("(")[1][:-1]
                if value_name=="":
                    value_data=getattr(Context(),func_name)()
                else:
                    value_data=getattr(Context(),func_name)(*value_name.split(","))
                regular_int_pattern = r'\'\${{(.*?)}}\''
                target = re.sub(regular_int_pattern,str(value_data),target,1)
            else:
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name =="":
                    value_data =getattr(Context(),func_name)()
                else:
                    value_data=getattr(Context(),func_name)(*value_name.split(","))
                target=re.sub(regular_pattern,str(value_data),target,1)
        return target
    except AttributeError:
        ERROR.logger.error("未找到对应要替换的数据，请检查数据是否正确 %s",target)
        raise
    except IndexError:
        ERROR.logger.error("yaml中的${{}} 函数方法不正确，正确愈发实例：${{get_time()}}")
        raise

if __name__ == '__main__':
    a = "${{host()}} aaa "
    b = regular(a)