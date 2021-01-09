from rest_framework import serializers
from blog.models import SharingFile

class SharingFileSerializer(serializers.ModelSerializer):
    class Meta():
        model = SharingFile
        fields =(
            'user',
            'sharing_type',
            'file',
            'title'
        )
