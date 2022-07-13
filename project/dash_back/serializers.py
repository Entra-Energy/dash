from rest_framework import serializers #type ignore
from datetime import datetime, timedelta, time
from dash_back.models import Post,Online,Price, Flexi #type ignore

class PostSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = Post
        value = serializers.FloatField()
        #fields = "__all__"
        fields = ('devId','value','created','created_date','grid')


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
