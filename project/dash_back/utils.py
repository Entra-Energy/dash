import json
import requests
from django.conf import settings
from dash_back.models import Price, FlexabilitySim, Flexi, Hydro, PostForecast, Post
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


def date_to_timestamp(date :str) -> int:   
    stamp = datetime.fromisoformat(date).timestamp()
    return int(stamp)

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

def post_forecast():
    pass



def price_to_db():
    price_path = os.path.join(settings.BASE_DIR, 'ibex.json')
    #print(price_path)
    with open(price_path, 'r') as f:
        my_json_obj = json.load(f)
    for data in my_json_obj:
        time = convert(data["time"])
        price = float(data["price"])
        #print(price)
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
            timer = int(obj.sched_durration)*60
            due_date = curr[:-1]
            stamp = date_to_timestamp(due_date)+timer            
            topic = str(dev+"/correction")
            single_data = {
                "power":pow,
                "due_sim_stamp":stamp
            }
            publish.single(topic, str(single_data), hostname="159.89.103.242", port=1883)
    else:
        print("There is no objects")
    actual_provide = Flexi.objects.filter(response_time=curr)
    if (actual_provide):
        for act_obj in actual_provide:
            dev_id = act_obj.flexiDev
            power = act_obj.res_pow
            duration = int(act_obj.res_durr)*60
            due_date_actual = curr[:-1]
            stamp_actual = date_to_timestamp(due_date_actual)+duration
            actual_topic = str(dev_id+"/actualProvide")
            actual_data = {
                "power":power,
                "due_stamp":stamp_actual
            }
            publish.single(actual_topic, str(actual_data), hostname="159.89.103.242", port=1883)
            

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
        "HY_GVOL":HY_GVOL,
        "HY_ALRM":0
    }    
    
    topic = 'hydro'
    publish.single(topic, str(hydro), hostname="159.89.103.242", port=1883)
    if power:
        count = Hydro.objects.all().count()
        # if count > 200:
        #     Hydro.objects.all().delete()
        Hydro.objects.create(hydro_pow=power,guide_vains=guide_vains,level=level,gen_temp=gen_tmp,gen_curr=gen_curr,gen_vol=gen_u)
        
    #return data
    
def get_pv():   
    def convert():
        todays_date = datetime.now()
        year = todays_date.year - 1
        month = 9
        day = 1
        month_curr = todays_date.month
        day_curr = todays_date.day
        hour = todays_date.hour 
        min = todays_date.minute
        sec = todays_date.second
        time_hour = datetime(year, month, day, hour, min, sec ,tzinfo=pytz.utc).timestamp()            
        toStr = str(time_hour).split(".")[0]
        int_stamp = int(toStr)
        time_hour_curr = datetime(year+1, month_curr, day_curr, hour, min, sec ,tzinfo=pytz.utc).timestamp()
        toStr_curr = str(time_hour_curr).split(".")[0]
        int_stamp_curr = int(toStr_curr)
        return [int_stamp,int_stamp_curr]
    
    test = os.path.join(settings.BASE_DIR, 'pv-data-new.json')    
    
    with open(test, 'r') as f:
        #d_old_str = f.read().replace('\n', '') # remove all \n
        my_json_obj = json.load(f)
        for data in my_json_obj:            
            timestamp_curr = convert()[0]
            if data["timestamp"] == timestamp_curr:                
                curr_ts = convert()[1]
                pv = {
                    "timestamp": curr_ts,
                    "PV_AP" : data["Power Active"],
                    "PV_RP" : data["Power Reactive"],
                    "PV_ET" : data["Temperature"],
                    "PV_WS" : data["Wind Speed"],
                    "PV_SI" : data["Solar Irradiance"],
                    "PV_ALRM" : data["alarm"],
                }
                topic = "pv/local"
                publish.single(topic, str(pv), hostname="159.89.103.242", port=1883)
                break
def timeSet():
    now_setTime = datetime.now(timezone('Europe/Sofia'))
    consum_obj = {
                    'setY': now_setTime.year,
                    'setM': now_setTime.month,
                    'setD':now_setTime.day,
                    'setH':now_setTime.hour,
                    'setmm':now_setTime.minute,
                    'setS':now_setTime.second                    
                }
    topic = "setRTC"
    publish.single(topic,str(consum_obj),hostname="159.89.103.242",port=1883)

def mqttErr(error_lst):
    er_list = error_lst
    post_list_init = []
    for obj in er_list:
        dev_id = obj["devId"]
        value = obj["value"]
        created = obj["created_date"]
        stamp = obj["timestamp"]
        exist = Post.objects.filter(created_date=created,devId = dev_id)
        if exist.count() == 1:
            topic = dev_id + "/timestamp"
            jObj = {
                "time": stamp,
                "pow": 0,
                }
            publish.single(topic, str(jObj), hostname="159.89.103.242", port=1883)
            
        else:
            p = Post(devId=dev_id,value=value,created_date=created)
            post_list_init.append(p)
            topic = dev_id + "/timestamp"
            jObj = {
                "time": stamp,
                "pow": 0,
                }
            publish.single(topic, str(jObj), hostname="159.89.103.242", port=1883)
    Post.objects.bulk_create(post_list_init)

       
    # data_out = json.loads(msg.decode())
    # timestamp = int(data_out['payload']['timestamp'])
    # timestamp_iso = datetime.fromtimestamp(timestamp).isoformat()
    # value = float(data_out['payload']['power'])    
    # exist = Post.objects.filter(created_date=timestamp_iso,devId = devId)
    # topic = devId + "/timestamp"
    # if exist.count() == 1:
    #     jObj = {
    #         "time": timestamp,
    #         "pow": 0,
    #         }
    #     publish.single(topic, str(jObj), hostname="159.89.103.242", port=1883)
    # else:
    #     Post.objects.create(devId=devId,value=value,created_date=timestamp_iso)



           
# def device_forecast():
#     PostForecast.objects.create(devId='sm-0002', value = )