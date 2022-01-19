from rest_framework import serializers #type ignore

from dash_back.models import Post,Online #type ignore

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class OnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online
        fields = "__all__"
