import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from account.models import *

from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def accountLogin(request):
    try:
        params = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"code": 400, "msg": "出现错误，请稍后重试", "data": None})
    account = Account.objects.filter(name=params['name']).first()
    # 判断是否有这个用户
    if account is None:
        return JsonResponse({"code": 410, "msg": "没有这个账号，请先进行用户注册", "data": None})
    # 用户存在，判断密码是否匹配
    elif account.password != params['password']:
        return JsonResponse({"code": 411, "msg": "账号或密码输入错误", "data": None})
    else:
        # 更新当日登录人数
        info = RegAndLogInfo.objects.filter(date=datetime.date.today()).first()
        if info is None:
            # 没有这一天的记录
            info = RegAndLogInfo(enrollment=0, login_number=1)
        else:
            info.login_number = info.login_number + 1
        info.save()
        request.session['loginAccount'] = account.name
        request.session.set_expiry(60 * 60 * 24)  # 登录状态保持24小时
        userinfo = {"name": account.name}
        return JsonResponse({"code": 200, "msg": "登录成功", "data": userinfo})


def accountLogout(request):
    request.session.flush()
    return JsonResponse({"code": 200, "msg": "退出登录成功", "data": None})


def accountRegister(request):
    try:
        params = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"code": 400, "msg": "出现错误，请稍后重试", "data": None})
    # 判断是否有这个用户
    account = Account.objects.filter(name=params['name']).first()
    if account is not None:
        return JsonResponse({"code": 420, "msg": "用户名已存在，请换个用户名", "data": None})
    else:
        account = Account(name=params['name'], password=params['password'])
        account.save()
        # 更新当日注册人数
        info = RegAndLogInfo.objects.filter(date=datetime.date.today()).first()
        if info is not None:
            info.enrollment = info.enrollment + 1
        else:
            info = RegAndLogInfo(enrollment=1, login_number=0)
        info.save()
        return JsonResponse({"code": 200, "msg": "注册成功", "data": None})


def checkLogin(request):
    print(request.session.items())
    loginAccount = request.session.get("loginAccount")
    if loginAccount is None:
        return JsonResponse({"code": 401, "msg": "未登录", "data": None})
    else:
        userinfo = {"name": loginAccount}
        return JsonResponse({"code": 200, "msg": "已登录", "data": userinfo})


def authenticate(request):
    """
    :param request: 请求
    :return: 当前请求是否登录
    """
    return True  # 测试
    if request.session.get("loginAccount") is not None:
        return True
    else:
        return False
