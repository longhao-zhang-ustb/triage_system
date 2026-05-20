# speechrecognition/urls.py

from django.urls import path
from digitaldoctor.views import *

urlpatterns = [
   path('', getAiSuggestions, name='getAiSuggestions')
]
