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

                #unique[elem.dev] = {'dev':elem.dev,'pow':elem.pow, 'ready':elem.ready, 'signal':elem.signal, 'providing':elem.providing,'date':elem.saved_date}
                unique[elem.dev] = {'dev':elem.dev,'ready':elem.ready,'pow':elem.pow, 'providing':elem.providing, 'dev_name':elem.dev_name, 'lat':elem.lat, 'long':elem.long}
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
        dataset = super().get_queryset().annotate(created=TruncHour('timestamp_aris')).values('created').annotate(power_aris=Avg('power_aris')).values('power_aris','created').annotate(wind_aris=Avg('wind_aris')).values('wind_aris','created','power_aris',).order_by('created')
        return dataset



class MonthPostManager(models.Manager):
    def get_queryset(self):
        dataset = super().get_queryset().annotate(created=TruncHour('created_date')).values('created').annotate(value=Avg('value')).values('devId','created','value','grid','actualCorr','actualProviding','providingAmount').order_by('created')
        return dataset

class MonthPostForecastManager(models.Manager):
    def get_queryset(self):
        dataset = super().get_queryset().annotate(created=TruncHour('created_date')).values('created').annotate(value=Avg('value')).values('devId','created','value').order_by('created')
        return dataset


class Post(models.Model):

    devId = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())
    value = models.FloatField()
    objects = models.Manager()
    grid = models.IntegerField(default=0, null=True)
    today = TodayPostManager()
    month = MonthPostManager()
    costH = models.FloatField(default=0, null=True)
    costD = models.FloatField(default=0, null=True)
    costM = models.FloatField(default=0, null=True)
    budgetH = models.IntegerField(default=0, null=True)
    budgetD = models.IntegerField(default=0, null=True)
    budgetM = models.IntegerField(default=0, null=True)
    actualCorr = models.FloatField(default=0, null=True)
    actualProviding = models.IntegerField(default=0, null=True)
    providingAmount = models.FloatField(default=0, null=True)
    
    def __str__(self):
        return self.devId
    
class PostForecast(models.Model):
    devId = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())
    value = models.FloatField()
    today = TodayPostManager()
    objects = models.Manager()
    month = MonthPostForecastManager()


class Online(models.Model):
    dev = models.CharField(max_length=300)
    saved_date = models.DateTimeField(default=datetime.now())
    pow = models.FloatField()
    ready = models.IntegerField(default=0, null=True)
    signal = models.IntegerField(default=0, null=True)
    providing = models.IntegerField(default=0, null=True)
    objects = models.Manager()
    dist = UniqueOnlineManager()
    dev_name = models.CharField(default='lab', max_length=300)
    lat = models.FloatField(default=0, null=True)
    long = models.FloatField(default=0, null=True)

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
    #requested_power = models.FloatField()

class Aris(models.Model):
    power_aris = models.FloatField()
    timestamp_aris = models.DateTimeField(default=datetime.now())
    wind_aris = models.FloatField()
    objects = models.Manager()
    today = TodayArisManager()
    month = MonthArisManager()

class Neykovo(models.Model):
    power_neykovo = models.FloatField()
    timestamp_neykovo = models.DateTimeField(default=datetime.now())
    wind_neykovo = models.FloatField()

class UserIp(models.Model):
    user_ip = models.CharField(max_length=900)
    
class Hydro(models.Model):
    timestamp_hydro = models.DateTimeField(default=datetime.now())
    hydro_pow = models.FloatField()
    guide_vains = models.FloatField()
    level = models.FloatField()
    gen_temp = models.FloatField()
    gen_curr = models.FloatField()
    gen_vol = models.FloatField()
    
class GridAsign(models.Model):
    dev = models.CharField(max_length=100)
    grid_name = models.CharField(max_length=300)
    