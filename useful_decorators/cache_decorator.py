import time
import math
import functools
import pickle
import hashlib
import requests
import os
from redis import Redis


def get_host():
    aliyun = '39.105.154.2'
    huaweiyun = '139.9.95.119'
    if os.name == 'posix':
        return aliyun
    else:
        return 'localhost'


def get_redis():
    host = get_host()
    redis = Redis(host=host)
    result = redis.set("xxx_{}".format(int(time.time())), time.time())
    print(result)
    return redis


cache = get_redis()


def _compute_key(function, args, kw):
    '''序列化并求其哈希值'''
    print((function.__name__, args, kw))
    print(pickle.dumps((function.__name__, args, kw)))
    return hashlib.md5(pickle.dumps((function.__name__, args, kw))).hexdigest()


def function_caches(times=60):
    def _memoize(function):
        @functools.wraps(function)  # 自动复制函数信息
        def __memoize(*args, **kw):
            force_updata = kw.pop("redis_force_updata", False)
            key = _compute_key(function, args, kw)
            if force_updata:
                # 运行函数
                result = function(*args, **kw)
                # 保存结果
                cache.set(key, pickle.dumps(result), times)
            else:
                # 是否已缓存？
                result = cache.get(key)
                if result:
                    result = pickle.loads(result)
                else:
                    # 运行函数
                    result = function(*args, **kw)
                    # 保存结果
                    cache.set(key, pickle.dumps(result), times)
            return result

        return __memoize

    return _memoize


@function_caches(times=20000)
def get_data(site='http://www.zhihu.com'):
    r = requests.get(site)
    text = r.text
    return text


if __name__ == '__main__':
    site = 'https://www.qq.com'
    data = get_data(site)
    print(data)
