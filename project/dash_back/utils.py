import json
from sqlite3 import Timestamp
import requests
from dash_back.models import Price, FlexabilitySim, Flexi
from datetime import datetime,tzinfo,timedelta
from datetime import date
import pytz
from pytz import timezone
from django.conf import settings
import os
import paho.mqtt.publish as publish

def get_curr_time():
    now = datetime.now(timezone('Europe/Sofia'))
    now = str(now)
    currDate = now.split(" ")[0]+"T"
    cur_hour = now.split(" ")[1].split(":")[0]
    cur_hour_min = now.split(" ")[1].split(":")[1]
    query_date = currDate+cur_hour+":"+cur_hour_min+":00Z"
    return query_date

def convert(str):
    todays_date = date.today()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day

    str = str.split(':')
    hour = int(str[0])
    #est = pytz.timezone('Europe/Sofia')
    time_hour = datetime(year, month, day, hour, 0, 0, tzinfo=pytz.utc)
    return time_hour

def price_to_db():
    price_path = os.path.join(settings.BASE_DIR, 'ibex.json')
    print(price_path)
    with open(price_path, 'r') as f:
        my_json_obj = json.load(f)
    for data in my_json_obj:
        time = convert(data["time"])
        price = float(data["price"])
        print(price)
        Price.objects.get_or_create(timestamp=time, value = price)

def scheduled_flexi():
    # test = FlexabilitySim.objects.all().last()
    # yourdate = test.scheduled
    curr = get_curr_time()
    sched_obj = FlexabilitySim.objects.filter(scheduled=curr)
    if(sched_obj):
        for obj in sched_obj:
            dev = obj.provided_dev
            pow = obj.sched_pow
            timer = obj.sched_durration
            topic = str(dev+"/correction")
            single_data = {
                "power":pow,
                "timer":timer
            }
            publish.single(topic, str(single_data), hostname="159.89.103.242", port=1883)
    else:
        print("There is no objects")

def exec_all():

    today = get_curr_time()
    future_reqs = Flexi.objects.filter(response_time__gte=today)
    if future_reqs:
        for req in future_reqs:
            dev_req = req.flexiDev
            scheduled_req = req.response_time
            pow_req = req.res_pow
            durr_req = req.res_durr
            FlexabilitySim.objects.get_or_create(provided_dev=dev_req,scheduled=scheduled_req,sched_pow=pow_req,sched_durration=durr_req)

def get_hydro():
    
    
    url = "https://api.thingspeak.com/channels/867128/feeds.json?api_key=9KHXETAXFJX8DWF9&results=2"

    r = requests.get(url)
    page_content = r.text
    # It turns out Flickr escapes single quotes (')
    # and apparently this isn't allowed and makes the JSON invalid.
    # we use String.replace to get around this
    probably_json = page_content.replace("\\'", "'")
    # now we load the json
    feed = json.loads(probably_json)
    data = feed["feeds"][-1]
    timestamp = data["created_at"]
    print (timestamp)
    #return data