import json
from dash_back.models import Price, FlexabilitySim
from datetime import datetime,tzinfo,timedelta
from datetime import date
import pytz
from pytz import timezone
from django.conf import settings
import os

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
            print(obj.provided_dev+"||"+str(obj.sched_pow)+"||"+str(obj.sched_durration))
    else:
        print("There is no objects")
