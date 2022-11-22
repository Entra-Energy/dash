from django.core.management.base import BaseCommand
import random
import json
from dash_back.models import Post, Online, Flexi, Aris #type: ignore
from paho.mqtt import client as mqtt_client #type: ignore
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from django.utils.timezone import activate
import pytz
from pytz import timezone
from django.db.models import Sum
#from pytz import timezone

class Command(BaseCommand):

    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        
        def validateJSON(jsonData):
            try:
                json.loads(jsonData)
            except ValueError as err:
                return False
            return True       
        
        def on_connect(client, userdata, flags, rc):
            #print("Connected with result code "+str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("data/#")
            client.subscribe("ping/#")
            client.subscribe("error/check/#")
            client.subscribe("flexiResponse/#")
            client.subscribe("corrResponse/#")
            client.subscribe("windData")
            client.subscribe("init/#")
            

        def on_message(client, userdata, msg):
            #print(msg.topic+" "+str(msg.payload))
            topic = msg.topic
            myList = topic.split('/')
            if myList[0] == 'data':
                dev_id = myList[1]
                is_valid = validateJSON(msg.payload)
                if is_valid:                      
                    data_out=json.loads(msg.payload.decode())                
                    timestamp = int(data_out['payload']['timestamp'])
                    timestamp = datetime.fromtimestamp(timestamp).isoformat()
                    value = float(data_out['payload']['power'])
                    readyness = int(data_out['payload']['gridReady'])
                   
                    costHour = data_out['payload'].get('costH', None)
                    if costHour:
                        costH = costHour
                    else:
                        costH = 0
                    costDay = data_out['payload'].get('costD', None)
                    if costDay:
                        costD = costDay
                    else:
                        costD = 0
                    costMonth = data_out['payload'].get('costM', None)
                    if costMonth:
                        costM = costMonth
                    else:
                        costM = 0                    
                    
                    budgetHour = data_out['payload'].get('budgetH', None)
                    if budgetHour:
                        budgetH = budgetHour
                    else:
                        budgetH = 0              
                    budgetDay = data_out['payload'].get('budgetD', None)                    
                    if budgetDay:
                        budgetD = budgetDay
                    else:
                        budgetD = 0   
                    budgetMonth= data_out['payload'].get('budgetM', None)                    
                    if budgetMonth:
                        budgetM = budgetMonth
                    else:
                        budgetM = 0               
                   

                Post.objects.get_or_create(devId=dev_id,value=value,created_date=timestamp,grid=readyness, costH = costH, costD = costD, costM = costM, budgetH = budgetH,budgetD = budgetD, budgetM = budgetM)

            if myList[0] == 'ping':                
                dev_id = myList[1]
                is_valid = validateJSON(msg.payload)
                if is_valid:      
                
                    data_out=json.loads(msg.payload.decode())
                    
                    timestamp = (data_out['payload'].get('timestamp', None))
                    if timestamp:
                        print(timestamp)
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()
                    else:
                        timestamp = 0
                    value = float(data_out['payload']['power'])
                    gridSupp = data_out['payload'].get('gridReady', None)
                    dev_name = data_out['payload'].get('blynkName', None)
                    lat = data_out['payload'].get('lat', None)
                    long = data_out['payload'].get('long', None)


                    if gridSupp:
                        ready = int(gridSupp)
                    else:
                        ready = 0
                    signal = data_out['payload'].get('signal', None)
                    if signal:
                        connectivity = int(signal)
                    else:
                        connectivity = 0
                    providing = data_out['payload'].get('providing', None)
                    if providing:
                        prov = int(providing)
                    else:
                        prov = 0
                    if dev_name:
                        name = str(dev_name)
                    else:
                        name = 'lab'
                    
                    if lat == "null" or lat == None:
                        latitude = 0.0
                    else:
                        latitude = float(lat)
                    if long == "null" or long == None:
                        longitude = 0.0
                    else:
                        longitude = float(long)
                    online = Online.objects.all().count()

                    if online > 1000:
                        Online.objects.all().delete()
                    #print(prov)
                    Online.objects.create(dev=dev_id, saved_date=timestamp, pow=value, ready=ready,signal=connectivity,providing = prov, dev_name = name, lat = latitude, long = longitude)

            if myList[0] == 'error':
                dev_id = myList[2]
                data_out = json.loads(msg.payload.decode())
                timestamp = int(data_out['payload']['timestamp'])
                timestamp_iso = datetime.fromtimestamp(timestamp).isoformat()
                value = float(data_out['payload']['power'])
                test = Post.objects.filter(created_date=timestamp_iso,devId = dev_id)
                topic = dev_id + "/timestamp"
                if test:
                    jObj = {
                    "time": timestamp,
                    "pow": value,
                    }
                    publish.single(topic, str(jObj), hostname="159.89.103.242", port=1883)

            if myList[0] == 'flexiResponse':
                dev_id = myList[1]
                data_out=json.loads(msg.payload.decode())
                time = int(data_out['payload']['date'])
                time_iso = datetime.fromtimestamp(time).isoformat()
                res_power = float(data_out['payload']['power'])
                durr = int(data_out['payload']['duration'])
                Flexi.objects.create(flexiDev = dev_id, response_time = time_iso, res_pow = res_power, res_durr = durr)


            # if myList[0] == 'corrResponse':
            #     dev_id = myList[1]
            #     data_out=json.loads(msg.payload.decode())
                #print(data_out)
            # if topic == 'windData':
            #     data_aris = json.loads(msg.payload.decode())
            #     wind = data_aris["wind"]
            #     wind = round(wind,2)
            #     power = data_aris["active"]
            #     power = round(power, 2)
            #     now = datetime.now()
            #     now = str(now)
            #     currDate = now.split(" ")[0]+"T"
            #     cur_hour = now.split(" ")[1].split(":")[0]
            #     cur_hour_min = now.split(" ")[1].split(":")[1]
            #     query_date = currDate+cur_hour+":"+cur_hour_min+":00Z"
            #     Aris.objects.create(power_aris=power,wind_aris=wind,timestamp_aris = query_date)
            
            if myList[0] == 'init':
                dev_id = myList[1]
                now = datetime.now(timezone('Europe/Sofia'))
                datem = str(datetime(now.year, now.month, 1))
                datem = datem.split(" ")[0]
                now = str(now)
                currDate = now.split(" ")[0]
                cur_hour = now.split(" ")[1].split(":")[0]
                query_hour = currDate+" "+cur_hour+":"+"00"
                for_last_hour = Post.objects.filter(created_date__gte=query_hour,devId = dev_id).aggregate(Sum('value'))
                if for_last_hour['value__sum']:                    
                    for_last_hour_consumption = float(for_last_hour['value__sum']/60)
                else:
                    for_last_hour_consumption = 0 
                
                for_today = Post.today.filter(devId=dev_id).aggregate(Sum('value'))
                if for_today['value__sum']:
                    for_today_consumption = float(for_today['value__sum']/60)
                else:
                    for_today_consumption = 0
                for_month = Post.month.filter(devId=dev_id,created__gte=datem).aggregate(Sum('value'))
                if for_month['value__sum']:
                    for_month_consumption = float(for_month['value__sum']/60)
                else:
                    for_month_consumption = 0
                last_obj = Post.objects.filter(devId = dev_id).last()
                if last_obj:
                    grid = int(last_obj.grid)
                    costPerH = float(last_obj.costH)
                    costPerD = float(last_obj.costD)
                    costPerM = float(last_obj.costM)
                    budgetPerH = int(last_obj.budgetH)
                    budgetPerD = int(last_obj.budgetD)
                    budgetPerM = int(last_obj.budgetM)
                    
                else:
                    grid = 0
                    costPerH = 0
                    costPerD = 0
                    costPerM = 0
                    budgetPerH = 0
                    budgetPerD = 0
                    budgetPerM = 0
                
                consum_obj = {
                    'for_hour':for_last_hour_consumption,
                    'for_today':for_today_consumption,
                    'for_month':for_month_consumption,
                    'ready':grid,
                    'costH':costPerH,
                    'costD':costPerD,
                    'costM':costPerM,
                    'budgetH':budgetPerH,
                    'budgetH':budgetPerD,
                    'budgetH':budgetPerM
                    
                }
                topic = "initial/"+dev_id
                publish.single(topic, str(consum_obj), hostname="159.89.103.242", port=1883)               
                


        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("159.89.103.242", 1883, 60)

        client.loop_forever()
