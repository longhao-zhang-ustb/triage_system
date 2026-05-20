from django.shortcuts import render
from django.http import JsonResponse
import os
from openai import OpenAI
# Create your views here.

def getAiSuggestions(request):
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'msg': '只允许POST请求'})
    # 获取body中的数据
    query_content = {}
    query_content['content'] = request.body.decode('utf-8')
    question = eval(query_content['content'])['question']
    image_urls = eval(query_content['content'])['photos']
    if image_urls == '':
        messages = [{'role': 'user', 'content': [{"type": "text", "text": question}]}]
    else:
        # 根据image_urls的长度生成content
        content = [{"type": "text", "text": question}]
        for i in range(len(image_urls)):
            content.append({"type": "image_url", "image_url": image_urls[i]})
        messages = [{'role': 'user', 'content': content}]    
    client = OpenAI(
        api_key="sk-b039d7bd13de46bb8b8bc29535a0e7eb",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen3.6-plus",
        messages=messages
    )
    # # 这里可以添加调用AI模型的逻辑，生成建议
    ai_suggestions = completion.choices[0].message.content
    return JsonResponse({'code': 0, 'msg': 'AI建议生成成功', 'content': ai_suggestions})
