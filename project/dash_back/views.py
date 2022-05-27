from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from dash_back.serializers import PostSerializer, OnlineSerializer, PriceSerializer
from dash_back.models import Post, Online, Price
from datetime import datetime
from dash_back.custom_filters import PostFilter, PriceFilter
import paho.mqtt.publish as publish

# class PostView(APIView):
#     # def get(self, request):
#     #     range = self.request.GET.get('range')
#     #     if range == '0':
#     #         posts = Post.today.all()
#     #     else:
#     #         posts = Post.month.all()
#     serializer = PostSerializer(posts, many=True)
#     # return Response({"posts": serializer.data})
class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_class = PostFilter
    search_fields = (
            '^devId',
        )


class  OnlineView(APIView):
    def get(self, request):
        online = Online.dist.all()

        serializer = OnlineSerializer(online, many=True)
        return Response({"online": serializer.data})


class PriceViewset(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_class = PriceFilter

@api_view(['POST',])
def post_data(request):
    my_data = request.data
    publish.single("correction", str(my_data), hostname="159.89.103.242", port=1883)
    return Response({"Success": "ok"})

@api_view(['POST',])
def post_cali(request):
    cali_data = request.data["calibrate"]

    for key in cali_data:
        topic = "cali/"+key
        val = cali_data[key]
        publish.single(topic, str(val), hostname="159.89.103.242", port=1883)
    return Response({"Success": "ok"})


@api_view(['POST',])
def post_single_correction(request):
    dev = request.data["dev"]
    pow = request.data["power"]
    timer = request.data["timer"]

    topic = str(dev+"/correction")
    single_data = {
        "power":pow,
        "timer":timer
    }
    publish.single(topic, str(single_data), hostname="159.89.103.242", port=1883)
    return Response({"Success": "ok"})

@api_view(['POST',])
def reset_data(request):
    reset_data = request.data["reset"]
    devId = reset_data['devId']
    topic = str(devId+"/reset")
    payload = reset_data["reset"]
    publish.single(topic, str(payload), hostname="159.89.103.242", port=1883)
    return Response({"Success": "ok"})
