from rest_framework import viewsets
from blog.models import SharingFile
from .serializers import SharingFileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SharingFileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=SharingFile.objects.all()
    serializer_class=SharingFileSerializer
    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
    