
from django.urls import path
from account.views import *

urlpatterns = [
    path('login', accountLogin),
    path('logout', accountLogout),
    path('register', accountRegister),
    path('check', checkLogin)
]
