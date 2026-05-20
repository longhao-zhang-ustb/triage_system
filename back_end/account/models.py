from django.db import models
from django.contrib import admin
# Create your models here.

class Account(models.Model):
    name = models.CharField('用户名', max_length=50, unique=True, null=False, blank=False)
    password = models.CharField('密码', max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'account'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

class RegAndLogInfo(models.Model):
    date = models.DateField('日期', auto_now_add=True)
    enrollment = models.IntegerField('当日注册人数')
    login_number = models.IntegerField('当日登录人数')

    class Meta:
        db_table = 'reg_log_info'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

admin.site.register(Account)
