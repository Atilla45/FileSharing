from django.shortcuts import render
from .serializers import SharingFileSerializer
from rest_framework import filters
from rest_framework import generics
from blog.models import SharingFile
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class SharingFileView(generics.ListCreateAPIView):
    
    queyset=SharingFile.objects.filter()
    serializer_class=SharingFileSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):  
        user=self.request.user
        queryset = SharingFile.objects.filter(user=user)
        sharing_type = self.request.query_params.get('sharing_type',None)
        print(queryset)
        return queryset
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)