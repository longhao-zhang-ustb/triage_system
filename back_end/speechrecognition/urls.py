# speechrecognition/urls.py

from django.urls import path
from speechrecognition.views import *

urlpatterns = [
   path('', getResult, name='getResult')
]
