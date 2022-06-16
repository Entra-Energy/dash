from django.core.management.base import BaseCommand
import random
import json
from dash_back.models import Post, Online #type: ignore
from paho.mqtt import client as mqtt_client #type: ignore
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

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
                online = Online.objects.all().count()
                if online > 1000:
                    Online.objects.all().delete()
                Online.objects.create(dev=dev_id, saved_date=timestamp, pow=value, ready=ready,signal=connectivity)

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
                print(data_out)
                print(dev_id)

            if myList[0] == 'corrResponse':
                dev_id = myList[1]
                data_out=json.loads(msg.payload.decode())
                print(data_out)



        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("159.89.103.242", 1883, 60)

        client.loop_forever()
