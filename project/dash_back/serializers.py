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
    class Meta:
        model = Aris
        wind_aris = serializers.FloatField()
        power_aris = serializers.FloatField()
        fields = ('created','timestamp_aris','power_aris','wind_aris')



class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"

class OnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online
        fields = ('saved_date','dev')

class FlexiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexi
        fields = "__all__"
