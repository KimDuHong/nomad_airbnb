from rest_framework.serializers import ModelSerializer
from .models import Photo
from rest_framework import serializers


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "description",
            "file",
        )
