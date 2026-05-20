from django.urls import path
from intelligenttriage.views import *

urlpatterns = [
   path('', getTriageResult, name='getTriageResult')
]
