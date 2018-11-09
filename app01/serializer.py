
from rest_framework import serializers
from app01.models import *

class PublishSerializers(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()

class PublishModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = "__all__"

class BookModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

