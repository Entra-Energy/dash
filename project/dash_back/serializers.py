from rest_framework import serializers #type ignore

from dash_back.models import Post,Online,Price, Flexi #type ignore

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"

class OnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online
        fields = "__all__"

class FlexiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexi
        fields = "__all__"
