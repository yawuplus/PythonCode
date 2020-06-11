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
    redis = Redis(host=host, password='Redis')
    return redis
