from multiprocessing.sharedctypes import Value
from rest_framework import serializers #type ignore
from datetime import datetime, timedelta, time
from dash_back.models import Post,Online,Price, Flexi, Aris, UserIp, PostForecast, FlexabilitySim, GridAsign, CapaAsign


class PostSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = Post
        value = serializers.FloatField()
        grid = serializers.IntegerField()
        actualCorr = serializers.FloatField()
        actualProviding = serializers.IntegerField()
        providingAmount = serializers.FloatField()
        # fields = "__all__"
        fields = ('devId','value','created_date','created','grid','actualCorr','actualProviding','providingAmount')


class ArisSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    class Meta:
        model = Aris
        wind_aris = serializers.FloatField()
        power_aris = serializers.FloatField()
        fields = ('created','timestamp_aris','power_aris','wind_aris')

class PostForecastSerializer(serializers.ModelSerializer):
     created = serializers.ReadOnlyField()
     class Meta:
         model = PostForecast
         value = serializers.FloatField()
         fields = ('devId','value','created_date','created')

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"

class OnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online
        fields = ('pow','dev','ready','providing','dev_name','lat','long')

class FlexiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexi
        fields = "__all__"
        
class FlexiSimSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlexabilitySim
        fields = "__all__"
        
class UserIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIp
        fields = "__all__"
class GridAsignSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridAsign
        fields = "__all__"

class CapaAsignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapaAsign
        fields = "__all__"
