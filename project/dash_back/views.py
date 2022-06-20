from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from dash_back.serializers import PostSerializer, OnlineSerializer, PriceSerializer, FlexiSerializer
from dash_back.models import Post, Online, Price, Flexi
from datetime import datetime
from dash_back.custom_filters import PriceFilter, PostFilter
import paho.mqtt.publish as publish
import time
import datetime as dt

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
        #print(serializer)
        return Response({"online": serializer.data})


class PriceViewset(viewsets.ModelViewSet):
    queryset = Price.objects.all()

    serializer_class = PriceSerializer
    filter_class = PriceFilter




class FlexiViewset(viewsets.ModelViewSet):
    queryset = Flexi.objects.all()
    serializer_class = FlexiSerializer



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


@api_view(['POST',])
def flexi_send(request):
    time_shift = 10800
    flexi_data = request.data
    dev = flexi_data['myObj']['dev']
    date = flexi_data['myObj']['date']
    date_part = date.split("T")[0]
    hour_part = date.split("T")[1]
    hours = hour_part.split(":")[0]
    mins = hour_part.split(":")[1]
    sec = ":00Z"
    time_part = hours+":"+mins+sec
    date_str = date_part+"T"+time_part
    t = time.mktime(dt.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").timetuple())
    t = str(t).split(".")[0]
    timestamp = int(t) + time_shift

    pow = flexi_data['myObj']['pow']
    duration = flexi_data['myObj']['duration']
    topic = dev+"/flexi"
    print(dev,date,pow,duration)
    if dev and date and pow and duration:
        payload = {
            "pow": pow,
            "duration": duration,
            "date": timestamp,
            "dev": dev
        }
        print(payload)
        publish.single(topic, str(payload), hostname="159.89.103.242", port=1883)
        return Response({"Success": "ok"})
