from django.shortcuts import render
from django.http import JsonResponse
import os
from datetime import datetime
from speechrecognition.client import XunfeiASRClient
from util.audioTrans import convert_webm_bytes_to_pcm_bytes
def getResult(request):

    if request.method != 'POST':
        return JsonResponse({'code': 405, 'msg': '只允许POST请求'})
    
    audio_file = request.FILES.get('audioFile')
    if not audio_file:
        return JsonResponse({'code': 400, 'msg': '未上传音频文件'})
    
    save_dir = r'upload_audios\\'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    pcm_filename = f"audio.pcm"
    pcm_file_path = os.path.join(save_dir, pcm_filename) 
    
    # 2. 转换 webm => pcm
    pcm_path = convert_webm_bytes_to_pcm_bytes(audio_file.read())
    # 写入pcm文件
    with open(pcm_file_path, 'wb') as f:
        f.write(pcm_path)
    try:
        # 调用科大讯飞语音识别, 此处替换为你自己的信息
        client = XunfeiASRClient(
            app_id="------",  
            api_key="------", 
            api_secret="------"
        )
        result = client.recognize(pcm_file_path, sample_rate=16000)
        return JsonResponse({'code': 0, 'msg': '音频识别成功', 'content': result['text']})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': f'音频识别失败：{str(e)}'})
