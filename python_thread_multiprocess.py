# _*_ coding: utf-8 _*_

"""
python_thread_multiprocee.py by xianhu
"""

import time
import threading
import multiprocessing

# 定义全局变量Queue
g_queue = multiprocessing.Queue()
g_search_list = list(range(10000))


# 定义一个IO密集型任务：利用time.sleep()
def task_io(task_id):
    print(f"IOTask[{task_id}] start")
    while not g_queue.empty():
        time.sleep(1)
        try:
            data = g_queue.get(block=True, timeout=1)
            print(f"IOTask[{task_id}] get data: {data}")
        except Exception as excep:
            print(f"IOTask[{task_id}] error: {str(excep)}")
    print(f"IOTask[{task_id}] end")
    return


# 定义一个计算密集型任务：利用一些复杂加减乘除、列表查找等
def task_cpu(task_id):
    print(f"CPUTask[{task_id}] start")
    while not g_queue.empty():
        count = sum(pow(3*2, 3*2) if i in g_search_list else 0 for i in range(10000))
        try:
            data = g_queue.get(block=True, timeout=1)
            print(f"CPUTask[{task_id}] get data: {data}")
        except Exception as excep:
            print(f"CPUTask[{task_id}] error: {str(excep)}")
    print(f"CPUTask[{task_id}] end")
    return task_id


def init_queue():
    print("init g_queue start")
    while not g_queue.empty():
        g_queue.get()
    for _index in range(10):
        g_queue.put(_index)
    print("init g_queue end")
    return


if __name__ == '__main__':
    print("cpu count:", multiprocessing.cpu_count(), "\n")

    print("========== 直接执行IO密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    task_io(0)
    print("结束：", time.time() - time_0, "\n")

    print("========== 多线程执行IO密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    thread_list = [threading.Thread(target=task_io, args=(i,)) for i in range(5)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        if t.is_alive():
            t.join()
    print("结束：", time.time() - time_0, "\n")

    print("========== 多进程执行IO密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    process_list = [multiprocessing.Process(target=task_io, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in process_list:
        p.start()
    for p in process_list:
        if p.is_alive():
            p.join()
    print("结束：", time.time() - time_0, "\n")

    print("========== 直接执行CPU密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    task_cpu(0)
    print("结束：", time.time() - time_0, "\n")

    print("========== 多线程执行CPU密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    thread_list = [threading.Thread(target=task_cpu, args=(i,)) for i in range(5)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        if t.is_alive():
            t.join()
    print("结束：", time.time() - time_0, "\n")

    print("========== 多进程执行cpu密集型任务 ==========")
    init_queue()
    time_0 = time.time()
    process_list = [multiprocessing.Process(target=task_cpu, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in process_list:
        p.start()
    for p in process_list:
        if p.is_alive():
            p.join()
    print("结束：", time.time() - time_0, "\n")

    exit()
