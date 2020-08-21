# coding: utf-8
from multiprocessing import Pool, cpu_count
import os
import time
import math


def task_func(data):
    for i in data:
        print("{} pid: {}".format(i, os.getpid()))


def long_time_task(i):
    print('子进程: {} - 任务{}'.format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


class RunProcessTask():
    cpu_num = cpu_count()

    def __init__(self, task_data, func, multiple=1):
        """
        100个url，2个cpu，进程数是CPU数的3倍，每个进程分 100/(2*3)
        """
        process_num = self.cpu_num * multiple
        print("func: ", func)
        task_data = self.split_data(task_data, int(math.ceil(
            len(task_data)/(multiple*self.cpu_num))))
        pool = Pool(process_num)
        print(task_data)
        for data in task_data:
            pool.apply_async(func, args=(data))
        pool.close()
        pool.join()
        print("finish task .")

    def split_data(self, data, per_size=10):
        target_list = []
        for i in range(int(math.ceil(len(data)/per_size))):
            start = i * per_size
            if start+per_size < len(data):
                end = start + per_size
            else:
                end = len(data)
            print("start {} end {}".format(start, end))
            per_list = data[start:end]
            if per_list:
                target_list.append(per_list)
        return target_list

    def long_time_task(self, i):
        print('子进程: {} - 任务{}'.format(os.getpid(), i))
        time.sleep(2)
        print("结果: {}".format(8 ** 20))


if __name__ == '__main__':
    data = [x for x in range(100)]
    task = RunProcessTask(data, long_time_task, 1)
