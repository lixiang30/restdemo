
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
    publish = serializers.HyperlinkedIdentityField(
        view_name="detailpublish",
        lookup_field="publish_id",
        lookup_url_kwarg="pk"
    )

class AuthorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

