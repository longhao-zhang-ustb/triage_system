from django.shortcuts import render
from django.http import JsonResponse
import asyncio
import threading
import time
import os
import json

class SharedLoop:
    _instance = None
    _loop = None
    _thread = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._loop = asyncio.new_event_loop()
            cls._thread = threading.Thread(target=cls._loop.run_forever, daemon=True)
            cls._thread.start()
        return cls._instance

    @property
    def loop(self):
        return self._loop

# 初始化全局共享loop
shared = SharedLoop()

# ==================== 全局变量 ====================
monitor = None
stop_event = threading.Event()

# ==================== 蓝牙异步任务 ====================
async def start_monitor():
    global monitor
    from vitalacquisition.bluetooth import VitalsMonitor
    monitor = VitalsMonitor()

    try:
        await monitor.start()
        connect_flag = 0

        while not stop_event.is_set():
            data = monitor.get_vitals()

            if connect_flag == 0 and any(v != "0" for v in data.values()):
                connect_flag = 1
                with open("vitalacquisition/check_bluetooth.txt", "w", encoding="utf-8") as f:
                    f.write("ok")

            if connect_flag:
                with open("vitalacquisition/vitals.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

            await asyncio.sleep(0.7)

    except Exception as e:
        print(f"蓝牙异常: {e}")

    finally:
        if monitor:
            try:
                await monitor.stop()
            except Exception:
                pass
        clear_files()
        print("蓝牙任务安全退出")

# ==================== 工具函数 ====================
def clear_files():
    for f in ["vitalacquisition/check_bluetooth.txt", "vitalacquisition/vitals.json"]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception:
            pass

# ==================== 连接蓝牙 ====================
def connectBluetooth(request):
    if request.method != "POST":
        return JsonResponse({"code": 405, "msg": "仅支持POST"})

    clear_files()
    stop_event.clear()

    # 把蓝牙任务丢到 永不关闭 的loop里
    asyncio.run_coroutine_threadsafe(start_monitor(), shared.loop)

    # 等待连接成功
    start = time.time()
    while time.time() - start < 100:
        if os.path.exists("vitalacquisition/check_bluetooth.txt"):
            return JsonResponse({"code": 200, "connect_status": "success", "msg": "连接成功"})
        time.sleep(0.5)

    # 超时
    stop_event.set()
    return JsonResponse({"code": 500, "connect_status": "error", "msg": "连接超时"})

# ==================== 断开蓝牙 ====================
def disconnectBluetooth(request):
    if request.method != "POST":
        return JsonResponse({"code": 405, "msg": "仅支持POST"})

    # 触发停止信号
    stop_event.set()

    # 等待1.5秒确保蓝牙停止
    time.sleep(1.5)

    clear_files()
    global monitor
    monitor = None

    return JsonResponse({"code": 200, "connect_status": "success", "msg": "蓝牙已断开"})

# ==================== 获取数据 ====================
def getBluetoothData(request):
    data = {}
    try:
        with open("vitalacquisition/vitals.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        pass
    return JsonResponse({"code": 200, "connect_status": "success", "data": data})
