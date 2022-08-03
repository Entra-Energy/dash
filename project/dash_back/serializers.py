from rest_framework import serializers #type ignore
from datetime import datetime, timedelta, time
from dash_back.models import Post,Online,Price, Flexi, Aris #type ignore

class PostSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = Post
        value = serializers.FloatField()
        grid = serializers.IntegerField()
        # fields = "__all__"
        fields = ('devId','value','created_date','created','grid')


class ArisSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    power = serializers.ReadOnlyField()
    wind = serializers.ReadOnlyField()
    class Meta:
        model = Aris
        #wind_aris = serializers.FloatField()
        fields = ('power','created','wind')



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
