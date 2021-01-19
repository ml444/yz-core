#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021-1-18
@desc: 数据结构模块
"""
from typing import List, Tuple


class ValuesSortDict(dict):
    """
    多值排序字典
    每次value更新都会重新排序
    """
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, super().__repr__())

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, key, value: List[Tuple]):
        if not isinstance(value, list):
            super().__setitem__(key, [value])
        else:
            super().__setitem__(key, value)

    def get(self, key, default=None):
        try:
            val = self[key]
        except KeyError:
            return default
        if val == []:
            return default
        return val

    def add(self, key, value: tuple):
        """

        :param key:
        :param value:
        :return:
        """
        if not isinstance(value, tuple):
            value = (value, -1)
        _values = self.__getitem__(key)
        result = self._sort_values(value, _values)
        self.__setitem__(key, result)

    def _sort_values(self, value: Tuple, _values: List[Tuple]) -> List[Tuple]:
        """

        :param value:
        :param _values:
        :return:
        """
        # one
        # _values.append(value)
        # return sorted(_values, key=lambda x: x[1], reverse=False)

        # two 推荐
        for i, v in enumerate(_values):
            if value[1] < v[1]:
                _values.insert(i, value)
                return _values
        _values.append(value)
        return _values

    def increase(self, key, v, inc=1):
        """
        自增元组值的序位
        :param key: 键
        :param v: 元组值的第一位
        :param inc:
        :return:
        """

        _values = self.__getitem__(key)

        if isinstance(v, str):  # 推荐
            for i, _v in enumerate(_values):
                if _v[0] == v:
                    _v = _values.pop(1)
                    _values.insert(i, (_v[0], _v[1]+inc))
                    return
            # 如果遍历结束还未返回，报错处理
            raise ValueError(f'The value[0]:[{v}] is not exist')

        elif isinstance(v, tuple) and len(v) == 2:
            try:
                _values.remove(v)
            except ValueError:
                pass
            # v[1] += inc
            self.__setitem__(key, self._sort_values((v[0], v[1]+inc), _values))
        else:
            raise ValueError(f'The value:[{v}] is error')



if __name__ == '__main__':
    import random
    # _values = [(f"ip{i}", random.randint(1, 10000)) for i in range(100000)]
    _values = [(f"ip{i}", i) for i in range(100000)]
    ipnum = random.randint(1, 100000)
    value = (f"ip{ipnum}", ipnum)
    print(value)
    import time

    d = ValuesSortDict()
    d["model"] = _values

    start = time.time()
    d.increase("model", value)
    end1 = time.time()
    d.increase("model", value[0])
    end2 = time.time()
    print("===>add:", end1-start)
    print("===>add0:", end2-end1)
