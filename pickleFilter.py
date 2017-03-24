#!/usr/bin/env python
# coding:utf-8
# author 9ian1i
# created at 2017.03.24
# a demo for filter unsafe callable object

from pickle import Unpickler as Unpkler
from pickle import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

# 修改以下白名单，确认你允许通过的可调用对象
allow_list = [str, int, float, bytes, unicode]


class FilterException(Exception):

    def __init__(self, value):
        super(FilterException, self).__init__('the callable object {value} is not allowed'.format(value=str(value)))


def _hook_call(func):
    """装饰器 用来在调用callable对象前进行拦截检查"""
    def wrapper(*args, **kwargs):
        if args[0].stack[-2] not in allow_list:
            # 我直接抛出自定义错误，改为你想做的事
            raise FilterException(args[0].stack[-2])
        return func(*args, **kwargs)
    return wrapper


# 重写了反序列化的两个函数
def load(file):
    unpkler = Unpkler(file)
    unpkler.dispatch[REDUCE] = _hook_call(unpkler.dispatch[REDUCE])
    return Unpkler(file).load()


def loads(str):
    file = StringIO(str)
    unpkler = Unpkler(file)
    unpkler.dispatch[REDUCE] = _hook_call(unpkler.dispatch[REDUCE])
    return unpkler.load()


def _filter_test():
    test_str = 'c__builtin__\neval\np0\n(S"os.system(\'net\')"\np1\ntp2\nRp3\n.'
    loads(test_str)

if __name__ == '__main__':
    _filter_test()
