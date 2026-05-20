from django.shortcuts import render
from django.http import JsonResponse
from vitalacquisition.bluetooth import VitalsMonitor
import time
import asyncio
import os
import threading
import json

# 异步蓝牙任务（独立运行）
async def start_monitor():
    global monitor
    monitor = VitalsMonitor()
    await monitor.start()
    flag = 0
    try:
        while True:
            v = monitor.get_vitals()
            if flag == 1:
                print('连接成功...')
                with open('vitalacquisition/check_bluetooth.txt', 'w') as f:
                    f.close()
            else:
                print('连接失败...')
            # 判断是否读到有效数据
            for k, val in v.items():
                if val != '0':
                    flag = 1
                print(f" {k}：{val}")
                with open('vitalacquisition/vitals.json', 'w') as f:
                    json.dump(v, f, ensure_ascii=False, indent=4)
            print('-' * 50)
            await asyncio.sleep(1)
            # 检测是否存在关闭连接的文件，如果存在，则关闭连接
            if os.path.exists('vitalacquisition/close_bluetooth.txt'):
                break
    except Exception as e:
        await monitor.stop()
    finally:
        # 关闭蓝牙监控
        print('关闭蓝牙监控...')
        os.remove('vitalacquisition/close_bluetooth.txt')
        await monitor.stop()

def run_async_in_background():
    asyncio.run(start_monitor())

# 改成 异步 Django视图
def connectBluetooth(request):
    # 只允许 POST
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'msg': '只允许POST请求', 'content': 'failed'})
    # 尝试删除 check_bluetooth.txt 文件，如果不存在也不报错
    try:
        os.remove('vitalacquisition/check_bluetooth.txt')
        os.remove('vitalacquisition/vitals.json')
    except FileNotFoundError:
        pass
    # 异步调用蓝牙
    thread = threading.Thread(target=run_async_in_background)
    thread.daemon = True  # 后台线程
    thread.start()
    # 循环检查 check_bluetooth.txt 文件是否存在，如果存在，说明连接成功
    # 获取当前时间，作为超时时间的参考
    start_time = time.time()
    while True:
        try:
            # 如果文件存在，说明连接成功
            if os.path.exists('vitalacquisition/check_bluetooth.txt'):
                return JsonResponse({'code': 200,'connect_status': 'success'})
        except FileNotFoundError:
            pass
        # 如果超过100秒，说明连接失败/超时
        if time.time() - start_time > 100:
            return JsonResponse({'code': 500,'connect_status': 'error'})

def getBluetoothData(request):
    if request.method != 'GET':
        return JsonResponse({'code': 405, 'msg': '只允许GET请求', 'content': 'failed'})
    # 读取vitals.json
    try:
        with open('vitalacquisition/vitals.json', 'r') as f:
            data = json.load(f)
            return JsonResponse({'code': 0, 'msg': '获取数据成功', 'data': data})
    except FileNotFoundError:
        return JsonResponse({'code': 500, 'msg': '未获取到设备数据', 'data': {}})
    
def disconnectBluetooth(request):
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'msg': '只允许POST请求', 'content': 'failed'})
    # 创建关闭连接文件
    with open('vitalacquisition/close_bluetooth.txt', 'w') as f:
        f.write('close')
        f.close()
    try:
        os.remove('vitalacquisition/check_bluetooth.txt')
        os.remove('vitalacquisition/vitals.json')
    except FileNotFoundError:
        pass
    return JsonResponse({'code': 200,'connect_status': 'success'})
