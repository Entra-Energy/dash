import json
from dash_back.models import Price, FlexabilitySim
from datetime import datetime,tzinfo,timedelta
from datetime import date
import pytz
from pytz import timezone
from django.conf import settings
import os
from dateutil import parser

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
    test = FlexabilitySim.objects.all()
    for t in test:
        yourdate = t.scheduled        
        print(yourdate)
