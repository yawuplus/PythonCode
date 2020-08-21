# coding: utf-8
from multiprocessing import Process
import os
import time


def long_time_task(i):
    print('子进程: {} - 任务{}'.format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__ == '__main__':
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    p1 = Process(target=long_time_task, args=(1,))
    p2 = Process(target=long_time_task, args=(2,))
    print('等待所有子进程完成。')
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print("总共用时{}秒".format((end - start)))
