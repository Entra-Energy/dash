import json
import requests
from django.conf import settings
from dash_back.models import Price, FlexabilitySim, Flexi, Hydro, PostForecast, Post, PostForecastMonth
from datetime import datetime,tzinfo,timedelta
from datetime import date
import pytz
from pytz import timezone
from django.conf import settings
import os
import paho.mqtt.publish as publish
import time
from django.core import management
import csv
from django.db.models import Avg
import calendar



def update_db_coeff():
    pass
    #date1 = "2023-05-23T00:00:00Z"
    # date2 = "2023-05-23T00:00:00Z"
    # id = 32710

    # delete_price = Price.objects.filter(id__gte=id)
    
    # delete_price.delete()
    # # date = "2023-05-09T00:00:00Z"
    # # delete_date = "2023-02-05T00:00:00Z" 
    # delete_query = Price.objects.filter(timestamp__lte=date2, timestamp__gte=date1)
    
    # delete_query.delete()
    # delete_query2 = Post.objects.filter(timestamp__lte = delete_date, devId = "sm-0030")
    # delete_query2.delete()
   
    # sms = ["sm-0012","sm-0014","sm-0017","sm-0018","sm-0019","sm-0020","sm-0030"]
    # for d in sms:
    #     if d == "sm-0012":                 
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
    #     elif d == "sm-0017":                       
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
    #     elif d == "sm-0018":
    #         delete_date = "2023-04-11T00:00:00Z"
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
    #     elif d == "sm-0019":
    #         delete_date = "2023-04-11T00:00:00Z"
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
    #     elif d == "sm-0020":
    #         delete_date = "2023-04-11T00:00:00Z"
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
    #     elif d == "sm-0014":
    #         delete_date = "2023-04-27T00:00:00Z"
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
    #     elif d == "sm-0030":
    #         delete_date = "2023-04-03T00:00:00Z"
    #         delete_query = Post.objects.filter(created_date__lte = delete_date, devId = d)        
    #         delete_query.delete()
            
            
    
#     # for obj in query:
#     #     #print(obj.id)     
#     #     u = Post.objects.get(id=obj.id)
#     #     print(u)
#     #     u.value = obj.value*120
#     #     u.save()         


sm_coeff = [{"sm-0001":120},{"sm-0002":320},{"sm-0003":400},{"sm-0004":200},{"sm-0006":200},{"sm-0008":200},{"sm-0009":80},
{"sm-0010":60},{"sm-0011":60},{"sm-0015":60},{"sm-0016":250},{"sm-0017":200},{"sm-0018":400},{"sm-0019":500},{"sm-0020":500},{"sm-0025":200}]         

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



# def price_to_db():
#     price_path = os.path.join(settings.BASE_DIR, 'ibex.json')
#     #print(price_path)
#     with open(price_path, 'r') as f:
#         my_json_obj = json.load(f)
#     for data in my_json_obj:
#         time = convert(data["time"])
#         price = float(data["price"])
#         #print(price)
#         Price.objects.get_or_create(timestamp=time, value = price)

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
            for d in sm_coeff:
                coeff = d.get(dev, None)
                if coeff:
                    pow = pow/coeff
                    pow = round(pow, 2)
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
            for d in sm_coeff:
                coeff = d.get(dev_id, None)
                if coeff:
                    power = power/coeff
                    power = round(power, 2)
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
    # now = datetime.now()

    # year_part = int(str(now).split(" ")[0].split("-")[0])
    # month_part = int(str(now).split(" ")[0].split("-")[1])
    # day_part = int(str(now).split(" ")[0].split("-")[2])

    # hour_part = int(str(now).split(" ")[1].split(":")[0])
    # min_part = int(str(now).split(" ")[1].split(":")[1])
    # sec_part = str(now).split(" ")[1].split(":")[2]

    # sec_part = float(sec_part)
    # sec_part = int(sec_part)
    # timestamp_now = datetime(year_part, month_part, day_part, hour_part, min_part, sec_part, tzinfo=pytz.utc).timestamp()    
    timestamp_now = round(time.time() * 1000)
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
        #Hydro.objects.create(hydro_pow=power,guide_vains=guide_vains,level=level,gen_temp=gen_tmp,gen_curr=gen_curr,gen_vol=gen_u)
        
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
                    "timestamp": curr_ts*1000,
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
        for d in sm_coeff:
            coeff = d.get(dev_id,None)
            if coeff:
                value = value*coeff
                value = round(value,2)       
        
        exist = Post.objects.filter(created_date=created,devId = dev_id,value=value)
        if exist.count() > 0:
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


def manage_comm():
    now = datetime.now(timezone('Europe/Sofia'))
    now = str(now)
    currDate = now.split(" ")[0]    
    
    exist = Price.objects.filter(timestamp__gte=currDate)
       
    if exist.first():
        pass
    else:
        
        management.call_command('crawl')    
    
    
def price_csv():
    #Price.objects.all().delete()
    test = os.path.join(settings.BASE_DIR, 'day-ahead.csv')    
    today = date.today()
    with open(test, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            date_p = row[0].split(" - ")[0]
            date_part = date_p.split(" ")[0]
            hour_part = "T"+date_p.split(" ")[1]+":00Z"
            date_convert = date_part.split(".")
            
            if len(date_convert) == 3:
                compare_date = date_convert[2]+"-"+date_convert[1]+"-"+date_convert[0] 
                past = datetime.strptime(compare_date, "%Y-%m-%d")
            
                if past.date() < today:    
                    date_fin = compare_date+hour_part       
                    
                    price = row[1]
                    if price:
                        bgn_price = float(row[1])*1.96
                        bgn_price = round(bgn_price, 2)                                            
                        exist = Price.objects.filter(timestamp=date_fin)       
                        if exist.first():
                            pass
                        else:
                            Price.objects.create(timestamp=date_fin, value=bgn_price)    
                            
                            
def fetch_simavi():
    
    url = 'http://ec2-35-180-235-215.eu-west-3.compute.amazonaws.com:8080/flexigrid/api/emax/data/bulgaria?deviceName=sm-0004&fromDate=2023-04-01 00:00:00&toDate=2023-05-31 00:00:00'
    response=requests.get(url)
    content = response.text
    json_data = content.replace("\\'", "'")
    data_feed = json.loads(json_data)    
    sm = data_feed.get("smartmeters")  
         
    #devs = ["sm-0006","sm-0007","sm-0009","sm-0010","sm-0011","sm-0012","sm-0013","sm-0014","sm-0015","sm-0016","sm-0017","sm-0018","sm-0019","sm-0020","sm-0022","sm-0024",] 
    
    for data in sm:   
        # start_date_str = '2023-04-26 17:00:00'
        # end_date_str = '2023-05-04 08:00:00'
        # start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
        # end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')      

        stamp = data.get("timestamp3m", None)
        date_part = stamp.split("T")[0]
        time_part = stamp.split("T")[1]
        time_helper = time_part.split("Z")[0] 
        str = date_part +" "+time_helper    
        datetime_object = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        power = data.get("power", None)        
        exist = Post.objects.filter(created_date=stamp,devId = "sm-0013",value=power)
        #if start_date < datetime_object < end_date:
       
        if exist.count() > 0:
            pass
        else:
            Post.objects.create(created_date=datetime_object,devId = "sm-0013",value=power)

# def forecast_day():
#     arr = []
#     dev = ''    
    
#     for i in range(0,31):
#         if i < 10:
#             dev = 'sm-000'+str(i)
#         else:
#             dev = 'sm-00' + str(i)
#         arr.append(dev)
#     for dev in arr:        
#         avg = Post.today.filter(devId=dev).aggregate(Avg('value'))
#         if isinstance(avg, dict):
#             avr = avg.get('value__avg', None)
#             if avr:
#                 current_datetime = datetime.now() - timedelta(days=1)

#                 # Get tomorrow's date
#                 tomorrow = current_datetime + timedelta(days=1)

#                 # Set the starting time to the beginning of tomorrow
#                 starting_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day)

#                 next_day = starting_time + timedelta(days=1)

#                 # Iterate over each minute
#                 while starting_time < next_day:                    
#                     starting_time += timedelta(minutes=1)
#                     PostForecast.objects.create(devId = dev+'F',created_date=starting_time, value=avr)
                    
                    
                    
                # PostForecast.objects.create(devId = dev+'F',created_date='2023-06-08T00:01:00', value=avr)
               
  
def forecast_today_calc(range, dev):
    if range == 'today':
        exist = PostForecast.today.filter(devId = dev+'F').count()
        print(exist)
        if exist == 0:
            avg = Post.today.filter(devId=dev).aggregate(Avg('value'))
            if isinstance(avg, dict):
                avr = avg.get('value__avg', None)
                if avr:
                    current_datetime = datetime.now() - timedelta(days=1)

                    # Get tomorrow's date
                    tomorrow = current_datetime + timedelta(days=1)

                    # Set the starting time to the beginning of tomorrow
                    starting_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day)

                    next_day = starting_time + timedelta(days=1)

                # Iterate over each minute
                while starting_time < next_day:                    
                    starting_time += timedelta(minutes=1)
                    PostForecast.objects.create(devId = dev+'F',created_date=starting_time, value=avr)
                    
    elif range == 'month':
        exist = PostForecastMonth.month.filter(devId = dev+'F').count()
        print(exist)
        if exist == 0:
            avg = Post.month.filter(devId=dev).aggregate(Avg('value'))
            if isinstance(avg, dict):
                avr = avg.get('value__avg', None)
                if avr:
                    now = datetime.now()
                    days_in_month = calendar.monthrange(now.year, now.month)[1]
                    today = now.day
                    days_till_month_end = days_in_month - today
                    month_start = now - timedelta(days=today-1)
                    month_end = now + timedelta(days=days_till_month_end)
                    starting_time = datetime(month_start.year, month_start.month, month_start.day)
                    finishing_time = datetime(month_end.year, month_end.month, month_end.day)
                while starting_time < finishing_time:
                    starting_time += timedelta(minutes=1)
                    PostForecastMonth.objects.create(devId = dev+'F',created_date=starting_time, value=avr)
                    
                
def clear_forecast_data(range, dev):
        if range == 'today':
            exist = PostForecast.today.filter(devId = dev+'F').count()
            print(exist)
            if exist > 0:
                PostForecast.today.filter(devId = dev+'F').delete()
                                    