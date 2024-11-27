#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
#-----------------------------------------------------------------------------
#                     --- TDOUYA STUDIOS ---
#-----------------------------------------------------------------------------
#
# @Project : pytest-training
# @File    : test_a.py
# @Author  : tianxin.xp@gmail.com
# @Date    : 2023/3/10 14:39
#
# 压力测试案例
#
#--------------------------------------------------------------------------"""
import threading
import time

import psutil
import pytest
import requests


# 定义测试用例
@pytest.mark.performance
def test_performance():
    # 设置测试参数
    url = 'http://www.tdouya.biz/'
    num_threads = 20
    num_requests = 200
    timeout = 5

    # 初始化测试结果
    response_times = []
    errors = 0
    successes = 0

    # 定义测试函数
    def test_func():
        nonlocal errors, successes
        for _ in range(num_requests):
            try:
                start_time = time.time()
                requests.get(url, timeout=timeout)
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                successes += 1
            except requests.exceptions.RequestException:
                errors += 1

                # 创建测试线程

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=test_func)
        threads.append(t)

        # 启动测试线程
    for t in threads:
        t.start()

        # 等待测试线程结束
    for t in threads:
        t.join()

        # 计算测试结果
    total_requests = num_threads * num_requests
    throughput = successes / (sum(response_times) or 1)
    concurrency = num_threads
    error_rate = errors / (total_requests or 1)
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    # 输出测试结果
    print(f'总请求数：{total_requests}')
    print(f'总时间：{sum(response_times):.2f}s')
    print(f'吞吐量：{throughput:.2f} requests/s')
    print(f'并发数：{concurrency}')
    print(f'错误率：{error_rate:.2%}')
    print(f'CPU利用率：{cpu_usage:.2f}%')
    print(f'内存利用率：{memory_usage:.2f}%')

    # 将测试结果写入文件
    with open(r'D:\workspace\pythonlearning\testoutput\performance_test_result.txt', 'w', encoding='utf-8') as fw:
        fw.write(f'总请求数：{total_requests}\n')
        fw.write(f'总时间：{sum(response_times):.2f}s\n')
        fw.write(f'吞吐量：{throughput:.2f} requests/s\n')
        fw.write(f'并发数：{concurrency}\n')
        fw.write(f'错误率：{error_rate:.2%}\n')
        fw.write(f'CPU利用率：{cpu_usage:.2f}%\n')
        fw.write(f'内存利用率：{memory_usage:.2f}%\n')
