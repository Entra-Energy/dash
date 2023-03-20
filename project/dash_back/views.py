from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from dash_back.serializers import PostSerializer, OnlineSerializer, PriceSerializer, FlexiSerializer, ArisSerializer, UserIpSerializer, PostForecastSerializer, FlexiSimSerializer
from dash_back.models import Post, Online, Price, Flexi, FlexabilitySim, Aris, UserIp, PostForecast
from datetime import datetime
from dash_back.custom_filters import PriceFilter, ArisFilter
from dash_back.tasks import task_exec_all
import paho.mqtt.publish as publish
import time
import datetime as dt
from pytz import timezone
#from dash_back.paginations import CustomPagination



# class ArisViewset(viewsets.ModelViewSet):
#     queryset = Aris.objects.all().order_by('timestamp_aris')
#
#     serializer_class = ArisSerializer
#     filter_class = ArisFilter


class userIpViewset(viewsets.ModelViewSet):    
    queryset = UserIp.objects.all()
    serializer_class = UserIpSerializer


class ArisViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        today = datetime.today()
        datem = str(datetime(today.year, today.month, 1))
        datem = datem.split(" ")[0]
        range = self.request.query_params.get('date_range',None)
        if range is not None:
            if range == 'today':
                queryset = Aris.today.all().order_by('timestamp_aris')
            if range == 'year':
                queryset = Aris.month.all()
            if range == 'month':
                queryset = Aris.month.filter(created__gte=datem)
            return queryset


    serializer_class = ArisSerializer


class PostViewset(viewsets.ModelViewSet):
    def get_queryset(self):

        #queryset = Post.objects.all()
        range = self.request.query_params.get('date_range',None)
        device = self.request.query_params.get('dev', None)
        today = datetime.today()
        datem = str(datetime(today.year, today.month, 1))
        datem = datem.split(" ")[0]

        if range is not None:
            if range == 'today':
                if device is not None:
                    queryset = Post.today.filter(devId=device).order_by('created_date')
                else:
                    queryset = Post.today.all().order_by('created_date')
                return queryset
            if range == 'year':
                if device is not None:
                    queryset = Post.month.filter(devId=device)
                else:
                    queryset = Post.month.all()
                return queryset
            if range == 'month':
                if device is not None:
                    queryset = Post.month.filter(devId=device,created__gte=datem)
                else:
                    queryset = Post.month.filter(created__gte=datem)
                return queryset
    #queryset = Post.objects.all()
    serializer_class = PostSerializer
    #pagination_class = CustomPagination

    # filter_class = PostFilter
    # search_fields = (
    #         '^devId',
    #     )

class PostForecastViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        range = self.request.query_params.get('date_range',None)
        device = self.request.query_params.get('dev', None)
        today = datetime.today()
        datem = str(datetime(today.year, today.month, 1))
        datem = datem.split(" ")[0]
        if range is not None:
            if range == 'today':
                if device is not None:
                    queryset = PostForecast.today.filter(devId=device).order_by('created_date')
                else:
                    queryset = PostForecast.today.all().order_by('created_date')
                return queryset
            if range == 'year':
                if device is not None:
                    queryset = PostForecast.month.filter(devId=device)
                else:
                    queryset = PostForecast.month.all()
                return queryset
            if range == 'month':
                if device is not None:
                    queryset = PostForecast.month.filter(devId=device,created__gte=datem)
                else:
                    queryset = PostForecast.month.filter(created__gte=datem)
                return queryset
    serializer_class = PostForecastSerializer

        
        


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
    queryset = Flexi.objects.all().order_by('-response_time')
    serializer_class = FlexiSerializer

class SimLogViewset(viewsets.ModelViewSet):    
    queryset = FlexabilitySim.objects.all().order_by('-scheduled')
    serializer_class = FlexiSimSerializer



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

#flexi sim
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

#flexi sim with calendar
@api_view(['POST',])
def sched_flexi(request):
    
    key='14252)5q?12FGs'
    sched_data = request.data
      
    key_received = sched_data['key']
    device = sched_data['dev']
    date_for_sched = sched_data['date']
    pow = sched_data['pow']
    duration = sched_data['duration']    
    # Put the requested power into new db field into FlexabilitySim
    #requested = Flexi.objects.filter(response_time=date_for_sched,flexiDev=device)
    #requested_pow = requested.res_pow
    if key_received == key:
        if device and date_for_sched and pow and duration:
            FlexabilitySim.objects.create(provided_dev=device,scheduled=date_for_sched,sched_pow=pow,sched_durration=duration)
            return Response({"Success": "ok"})



@api_view(['POST',])
def reset_data(request):
    reset_data = request.data["reset"]
    print(reset_data)
    devId = reset_data['devId']
    topic = str(devId+"/reset")
    payload = reset_data["reset"]
    publish.single(topic, str(payload), hostname="159.89.103.242", port=1883)
    return Response({"Success": "ok"})


@api_view(['POST',])
def flexi_send(request):
    
    key='14252)5q?12FGs'    
    flexi_data = request.data    
    dev = flexi_data.get("dev",None)
    date = flexi_data.get("date",None)
    pow = flexi_data.get('pow',None)
    duration = flexi_data.get('duration',None)
    print(date)
    print(dev)
    # time_shift = 7200
    # date_part = date.split("T")[0]
    # hour_part = date.split("T")[1]
    # hours = hour_part.split(":")[0]
    # mins = hour_part.split(":")[1]
    # sec = ":00Z"
    # time_part = hours+":"+mins+sec
    # date_str = date_part+"T"+time_part
    # t = time.mktime(dt.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").timetuple())
    # t = str(t).split(".")[0]
    # timestamp = int(t) + time_shift   
    # date_to_import = datetime.fromtimestamp(timestamp).isoformat() 
    key_received = flexi_data['key']
    if key_received == key:
        if dev and date and pow and duration:
            Flexi.objects.create(flexiDev = dev, response_time = date, res_pow = pow, res_durr = duration)
            return Response({"Success": "ok"})      
    
    # topic = dev+"/flexi"
    # print(dev,date,pow,duration)
    # if key_received == key:
    #     if dev and date and pow and duration:
    #         payload = {
    #             "pow": pow,
    #             "duration": duration,
    #             "date": timestamp,
    #             "dev": dev
    #         }
    #         print(payload)
    #         publish.single(topic, str(payload), hostname="159.89.103.242", port=1883)
            


@api_view(['POST',])
def login_data(request):
    print("Test!!!!")
    login_data = request.data
    print(login_data)
    username = login_data["login"]['username']
    password = login_data["login"]["password"]
    ip = login_data["login"]["ip"]
    if username == 'admin' and password == 'aA12121212':   
        print(ip)
        UserIp.objects.get_or_create(user_ip=ip)
        return Response({"Success": "ok"})

@api_view(['POST',])
def exec_all(request):
    req_data = request.data["execAll"]
    if(req_data == 'all'):
        task_exec_all.delay()


    return Response({"Success": "ok"})
