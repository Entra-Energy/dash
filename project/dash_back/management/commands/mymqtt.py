from django.core.management.base import BaseCommand
import random
import json
from dash_back.models import Post, Online, Flexi, Aris #type: ignore
from paho.mqtt import client as mqtt_client #type: ignore
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from django.utils.timezone import activate
#from pytz import timezone

class Command(BaseCommand):

    help = 'Displays current time'

    def handle(self, *args, **kwargs):
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

        def on_message(client, userdata, msg):
            #print(msg.topic+" "+str(msg.payload))
            topic = msg.topic
            myList = topic.split('/')
            if myList[0] == 'data':
                dev_id = myList[1]
                data_out=json.loads(msg.payload.decode())

                timestamp = int(data_out['payload']['timestamp'])
                timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
                value = float(data_out['payload']['power'])
                readyness = int(data_out['payload']['gridReady'])

                Post.objects.get_or_create(devId=dev_id,value=value,created_date=timestamp,grid=readyness)

            if myList[0] == 'ping':
                dev_id = myList[1]
                data_out=json.loads(msg.payload.decode())
                print(data_out)
                timestamp = int(data_out['payload']['timestamp'])
                timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
                value = float(data_out['payload']['power'])
                gridSupp = data_out['payload'].get('gridReady', None)


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
                online = Online.objects.all().count()

                if online > 1000:
                    Online.objects.all().delete()
                #print(prov)
                Online.objects.create(dev=dev_id, saved_date=timestamp, pow=value, ready=ready,signal=connectivity,providing = prov)

            if myList[0] == 'error':
                dev_id = myList[2]
                data_out = json.loads(msg.payload.decode())
                timestamp = int(data_out['payload']['timestamp'])
                timestamp_iso = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
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
                time_iso = datetime.fromtimestamp(time, tz=timezone.utc).isoformat()
                res_power = float(data_out['payload']['power'])
                durr = int(data_out['payload']['duration'])
                Flexi.objects.create(flexiDev = dev_id, response_time = time_iso, res_pow = res_power, res_durr = durr)


            if myList[0] == 'corrResponse':
                dev_id = myList[1]
                data_out=json.loads(msg.payload.decode())
                #print(data_out)
            if topic == 'windData':
                data_aris = json.loads(msg.payload.decode())
                wind = data_aris["wind"]
                wind = round(wind,2)
                power = data_aris["active"]
                power = round(power, 2)
                now = datetime.now()
                now = str(now)
                currDate = now.split(" ")[0]+"T"
                cur_hour = now.split(" ")[1].split(":")[0]
                cur_hour_min = now.split(" ")[1].split(":")[1]
                query_date = currDate+cur_hour+":"+cur_hour_min+":00Z"
                Aris.objects.create(power_aris=power,wind_aris=wind,timestamp_aris = query_date)


        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("159.89.103.242", 1883, 60)

        client.loop_forever()
