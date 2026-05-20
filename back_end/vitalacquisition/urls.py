
from django.urls import path
from vitalacquisition.views import *

urlpatterns = [
   path('connect/', connectBluetooth, name='connectBluetooth'),
   path('disconnect/', disconnectBluetooth, name='disconnectBluetooth'),
   path('getvitalData/', getBluetoothData, name='getBluetoothData')
]