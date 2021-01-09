from django.urls import path,include
from api.views import *

urlpatterns=[
    path('share/',SharingFileView.as_view(),name='share')
]