from django.core.management.base import BaseCommand
import random
import json
from dash_back.models import Post, Online #type: ignore
from paho.mqtt import client as mqtt_client #type: ignore
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

class Command(BaseCommand):

    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("data/#")
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload))
            topic = msg.topic
            myList = topic.split('/')

            dev_id = myList[1]
            data_out=json.loads(msg.payload.decode())
            timestamp = int(data_out['payload']['timestamp'])
            timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

            value = float(data_out['payload']['power'])
            print(data_out,dev_id)
            Post.objects.get_or_create(devId=dev_id,value=value, created_date=timestamp)
            Online.objects.get_or_create(dev=dev_id, saved_date=timestamp, pow=value)
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("159.89.103.242", 1883, 60)

        client.loop_forever()
