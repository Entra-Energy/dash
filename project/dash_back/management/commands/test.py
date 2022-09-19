from re import T
from django.core.management.base import BaseCommand
import json

from django.conf import settings
from datetime import datetime,tzinfo,timedelta
from datetime import date
import pytz
from pytz import timezone
import os
class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        # print(settings.BASE_DIR)
        def convert():
            todays_date = datetime.now()
            year = todays_date.year
            month = 9
            day = 1
            hour = todays_date.hour 
            min = todays_date.minute
            sec = todays_date.second           

            #str = str.split(':')
           
            #est = pytz.timezone('Europe/Sofia')
            time_hour = datetime(year, month, day, hour, min, sec ,tzinfo=pytz.utc).timestamp()    
            toStr = str(time_hour).split(".")[0]
            int_stamp = int(toStr)-10800
            return int_stamp

        test = os.path.join(settings.BASE_DIR, 'pv-data.json')
        t = convert()
        
        #priceJson = [json.loads(line) for line in open(test,'r')]
        with open(test, 'r') as f:
            #d_old_str = f.read().replace('\n', '') # remove all \n
            my_json_obj = json.load(f)


        for data in my_json_obj:            
            if data["timestamp"] == 1661979605:
                print(data["Temperature"])
            
            
