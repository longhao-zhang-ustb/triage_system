
from django.urls import path
from saveInfo.views import *

urlpatterns = [
   path('', save2Neo4j, name='save2Neo4j')
]