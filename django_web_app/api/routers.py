from django.urls import include, path
from rest_framework import routers
from api.views import *
from api.viewset import *

router = routers.DefaultRouter()
router.register(r'share', SharingFileView)