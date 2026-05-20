# -*- coding:utf-8 -*-
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2


class XunfeiASRClient:
    def __init__(self, app_id, api_key, api_secret):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.result_text = ""  # 存储最终识别结果
        self.all_results = []  # 存储所有识别片段
        self.is_finished = False
        self.error_msg = None
        
    class WsParam:
        def __init__(self, parent, audio_file, sample_rate=16000):
            self.parent = parent
            self.audio_file = audio_file
            self.sample_rate = sample_rate
            self.common_args = {"app_id": parent.app_id}
            self.business_args = {
                "domain": "iat",
                "language": "zh_cn",
                "accent": "mandarin",
                "vinfo": 1,
                "vad_eos": 10000
            }
        
        def create_url(self):
            url = 'wss://ws-api.xfyun.cn/v2/iat'
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))
            
            signature_origin = "host: ws-api.xfyun.cn\n"
            signature_origin += "date: " + date + "\n"
            signature_origin += "GET /v2/iat HTTP/1.1"
            
            signature_sha = hmac.new(
                self.parent.api_secret.encode('utf-8'),
                signature_origin.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()
            signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
            
            authorization_origin = f'api_key="{self.parent.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
            
            v = {
                "authorization": authorization,
                "date": date,
                "host": "ws-api.xfyun.cn"
            }
            return url + '?' + urlencode(v)
    
    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            code = data.get("code")
            sid = data.get("sid")
            
            if code != 0:
                self.error_msg = data.get("message", "未知错误")
                print(f"错误 - sid:{sid}, code:{code}, msg:{self.error_msg}")
                ws.close()
            else:
                # 提取识别结果
                if "data" in data and "result" in data["data"]:
                    result_data = data["data"]["result"]["ws"]
                    if result_data:
                        # 解析当前片段的结果
                        fragment = ""
                        for i in result_data:
                            for w in i["cw"]:
                                fragment += w["w"]
                        
                        if fragment:
                            self.all_results.append(fragment)
                            self.result_text = "".join(self.all_results)
                            print(f"识别中: {self.result_text}")
                
                # 检查是否识别完成
                if data.get("data", {}).get("status") == 2:
                    self.is_finished = True
                    print("识别完成!")
                    ws.close()
                    
        except Exception as e:
            print(f"解析消息异常: {e}")
            self.error_msg = str(e)
    
    def on_error(self, ws, error):
        print(f"WebSocket错误: {error}")
        self.error_msg = str(error)
    
    def on_close(self, ws, a, b):
        print("连接已关闭")
    
    def on_open(self, ws):
        def run():
            frame_size = 8000  # 每帧大小（字节）
            interval = 0.04    # 发送间隔（秒）
            status = STATUS_FIRST_FRAME
            
            with open(self.audio_file, "rb") as fp:
                while True:
                    buf = fp.read(frame_size)
                    
                    if not buf:
                        status = STATUS_LAST_FRAME
                    
                    # 第一帧
                    if status == STATUS_FIRST_FRAME:
                        d = {
                            "common": self.ws_param.common_args,
                            "business": self.ws_param.business_args,
                            "data": {
                                "status": 0,
                                "format": f"audio/L16;rate={self.ws_param.sample_rate}",
                                "audio": base64.b64encode(buf).decode('utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                        status = STATUS_CONTINUE_FRAME
                    
                    # 中间帧
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {
                            "data": {
                                "status": 1,
                                "format": f"audio/L16;rate={self.ws_param.sample_rate}",
                                "audio": base64.b64encode(buf).decode('utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                    
                    # 最后一帧
                    elif status == STATUS_LAST_FRAME:
                        d = {
                            "data": {
                                "status": 2,
                                "format": f"audio/L16;rate={self.ws_param.sample_rate}",
                                "audio": base64.b64encode(buf).decode('utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    
                    time.sleep(interval)
            
            # 等待服务端返回最后结果
            time.sleep(0.5)
            ws.close()
        
        thread.start_new_thread(run, ())
    
    def recognize(self, audio_file, sample_rate=16000):
        """
        识别音频文件
        
        Args:
            audio_file: PCM音频文件路径
            sample_rate: 采样率（8000或16000）
        
        Returns:
            str: 识别出的文本
        """
        # 重置状态
        self.result_text = ""
        self.all_results = []
        self.is_finished = False
        self.error_msg = None
        self.audio_file = audio_file
        
        # 创建参数
        self.ws_param = self.WsParam(self, audio_file, sample_rate)
        
        # 创建WebSocket连接
        ws_url = self.ws_param.create_url()
        websocket.enableTrace(False)
        
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.on_open = self.on_open
        
        # 运行连接
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        # 返回结果
        if self.error_msg:
            return {"success": False, "error": self.error_msg, "text": ""}
        else:
            return {"success": True, "text": self.result_text, "error": None}