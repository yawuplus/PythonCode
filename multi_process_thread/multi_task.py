#coding: utf-8
import time
import os


def long_time_task():
    print('当前进程: {}'.format(os.getpid()))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__ == "__main__":
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    for i in range(2):
        long_time_task()

    end = time.time()
    print("用时{}秒".format((end-start)))
