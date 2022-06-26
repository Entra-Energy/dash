import json
from dash_back.models import Price
from datetime import datetime,tzinfo,timedelta
from datetime import date
import pytz
from pytz import timezone
import os

def convert(self, str):
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
