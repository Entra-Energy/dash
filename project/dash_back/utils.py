import json
import requests
from django.conf import settings
from dash_back.models import Price, FlexabilitySim, Flexi, Hydro
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
    #iso_date = data["created_at"]
    power = data["field1"]
    guide_vains = data["field2"]
    level = data["field3"]
    gen_tmp = data["field4"]
    gen_u = data["field5"]
    gen_curr = data["field6"]
    
    #date_part = iso_date.split("T")[0].split("-")

    # year = int(date_part[0])
    # month = int(date_part[1])
    # day = int(date_part[2])

    # hour_part = iso_date.split("T")[1].split(":")

    # hour = int(hour_part[0])
    # last_min = int(hour_part[1])
    now = datetime.now()

    year_part = int(str(now).split(" ")[0].split("-")[0])
    month_part = int(str(now).split(" ")[0].split("-")[1])
    day_part = int(str(now).split(" ")[0].split("-")[2])

    hour_part = int(str(now).split(" ")[1].split(":")[0])
    min_part = int(str(now).split(" ")[1].split(":")[1])
    sec_part = str(now).split(" ")[1].split(":")[2]

    sec_part = float(sec_part)
    sec_part = int(sec_part)
    timestamp_now = datetime(year_part, month_part, day_part, hour_part, min_part, sec_part, tzinfo=pytz.utc).timestamp()    
    stamp = str(timestamp_now)
    HY_PW = str(power)
    HY_GV = str(guide_vains)
    HY_WL = str(level)
    HY_GT = str(gen_tmp)
    HY_GC = str(gen_curr)
    HY_GVOL = str(gen_u)
    hydro = {
        "timestamp":stamp,
        "HY_PW":HY_PW,
        "HY_GV":HY_GV,
        "HY_WL":HY_WL,
        "HY_GT":HY_GT,
        "HY_GC":HY_GC,
        "HY_GVOL":HY_GVOL
    }    
    
    topic = 'hydro'
    publish.single(topic, str(hydro), hostname="159.89.103.242", port=1883)
    if power:
        count = Hydro.objects.all().count()
        if count > 200:
            Hydro.objects.all().delete()
        Hydro.objects.create(hydro_pow=power,guide_vains=guide_vains,level=level,gen_temp=gen_tmp,gen_curr=gen_curr,gen_vol=gen_u)
        
    #return data
    
def get_pv():
    def convert():
        todays_date = datetime.now()
        year = todays_date.year
        month = 9
        day = 1
        hour = todays_date.hour 
        min = todays_date.minute
        sec = todays_date.second
        time_hour = datetime(year, month, day, hour, min, sec ,tzinfo=pytz.utc).timestamp()    
        toStr = str(time_hour).split(".")[0]
        int_stamp = int(toStr)
        return int_stamp
    
    test = os.path.join(settings.BASE_DIR, 'pv-data.json')
    with open(test, 'r') as f:
        #d_old_str = f.read().replace('\n', '') # remove all \n
        my_json_obj = json.load(f)
        for data in my_json_obj:
            timestamp_curr = convert()            
            if data["timestamp"] == timestamp_curr:
                pv = {
                    "timestamp": data["timestamp"],
                    "pow_active" : data["Power Active"],
                    "pow_react" : data["Power Reactive"],
                    "temp" : data["Temperature"],
                    "wind_spd" : data["Wind Speed"],
                    "irradiance" : data["Solar Irradiance"],
                    "alarm" : data["alarm"],
                }
                topic = "pv/local"
                publish.single(topic, str(pv), hostname="159.89.103.242", port=1883)
                