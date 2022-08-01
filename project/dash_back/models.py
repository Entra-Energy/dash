from django.db import models
from datetime import datetime, timedelta, time
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import activate
from pytz import timezone
import pytz
from django.db.models import Avg
from django.db.models.functions import TruncHour


class UniqueOnlineManager(models.Manager):
    def get_queryset(self):
        now = datetime.now(timezone('Europe/Sofia'))
        ten_minutes_ago = now - timedelta(minutes=5)
        ten_minutes_ago = str(ten_minutes_ago)
        currDate = ten_minutes_ago.split(" ")[0]+"T"
        cur_hour = ten_minutes_ago.split(" ")[1].split(":")[0]
        cur_hour_min = ten_minutes_ago.split(" ")[1].split(":")[1]
        query_date = currDate+cur_hour+":"+cur_hour_min+":00Z"

        last_active = super().get_queryset().filter(saved_date__gte = query_date)
        unique = {}
        for elem in reversed(last_active):
            if elem.dev not in unique.keys():

                unique[elem.dev] = {'dev':elem.dev,'pow':elem.pow, 'ready':elem.ready, 'signal':elem.signal, 'providing':elem.providing}
        print(unique.values())
        return unique.values()
        #return super().get_queryset().filter(dev__in = unique).order_by('-saved_date')[:len(unique)]



class TodayPostManager(models.Manager):

    def get_queryset(self):
        today = datetime.now(timezone('Europe/Sofia')).date()
        tomorrow = today + timedelta(1)
        today_start = str(today)+'T'+'00:00:00Z'
        today_end = str(tomorrow)+'T'+'00:00:00Z'
        print(today_start,today_end)
        return super().get_queryset().filter(created_date__gt = today_start, created_date__lt = today_end)


class TodayArisManager(models.Manager):

    def get_queryset(self):
        today = datetime.now(timezone('Europe/Sofia')).date()
        tomorrow = today + timedelta(1)
        today_start = str(today)+'T'+'00:00:00Z'
        today_end = str(tomorrow)+'T'+'00:00:00Z'
        return super().get_queryset().filter(timestamp_aris__gt = today_start, timestamp_aris__lt = today_end)

class MonthArisManager(models.Manager):

    def get_queryset(self):
        dataset = super().get_queryset().annotate(created=TruncHour('timestamp_aris')).values('created').annotate(power=Avg('power_aris')).values('created','power','wind_aris').order_by('created')    
        return dataset




class MonthPostManager(models.Manager):

    #start = datetime.combine(month_begin, time()) + timedelta(1)

    #end = datetime.combine(tomorrow, time())

    def get_queryset(self):
        dataset = super().get_queryset().annotate(created=TruncHour('created_date')).values('created').annotate(value=Avg('value')).values('devId','created','value','grid').order_by('created')
        #print(dataset)
        return dataset



        # today_day = datetime.now(timezone('Europe/Sofia')).day-1
        # today = datetime.now(timezone('Europe/Sofia')).date()
        # now = datetime.now(timezone('Europe/Sofia'))
        # now = str(now)
        # cur_hour = now.split(" ")[1].split(":")[0]
        # cur_min = now.split(" ")[1].split(":")[1]
        # till_now = str(today)+'T'+cur_hour+":"+cur_min+":00Z"
        # month_begin = today - timedelta(today_day)
        # start = str(month_begin) + 'T' + '00:00:00Z'
        # return super().get_queryset().filter(created_date__gt = start, created_date__lt = till_now)

class Post(models.Model):

    devId = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())
    value = models.FloatField()
    objects = models.Manager()
    grid = models.IntegerField(default=0, null=True)
    today = TodayPostManager()
    month = MonthPostManager()
    def __str__(self):
        return self.devId


class Online(models.Model):
    dev = models.CharField(max_length=300)
    saved_date = models.DateTimeField(default=datetime.now())
    pow = models.FloatField()
    ready = models.IntegerField(default=0, null=True)
    signal = models.IntegerField(default=0, null=True)
    providing = models.IntegerField(default=0, null=True)
    objects = models.Manager()
    dist = UniqueOnlineManager()

class Price(models.Model):
    timestamp = models.DateTimeField(default=datetime.now())
    value = models.FloatField()


class Flexi(models.Model):
    flexiDev = models.CharField(max_length=300)
    response_time = models.DateTimeField(default=datetime.now())
    res_pow = models.FloatField()
    res_durr = models.IntegerField()

class FlexabilitySim(models.Model):
    provided_dev = models.CharField(max_length=300)
    scheduled = models.DateTimeField(default=datetime.now())
    sched_pow = models.FloatField()
    sched_durration = models.IntegerField()

class Aris(models.Model):
    power_aris = models.FloatField()
    timestamp_aris = models.DateTimeField(default=datetime.now())
    wind_aris = models.FloatField()
    today = TodayArisManager()
    month = MonthPostManager()

class Neykovo(models.Model):
    power_neykovo = models.FloatField()
    timestamp_neykovo = models.DateTimeField(default=datetime.now())
    wind_neykovo = models.FloatField()
