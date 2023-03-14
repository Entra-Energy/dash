# from celery.task.schedules import crontab # type: ignore
# from celery.decorators import periodic_task # type: ignore
from celery.utils.log import get_task_logger # type: ignore
from celery import shared_task #type: ignore

from dash_back.utils import price_to_db, scheduled_flexi, exec_all, get_hydro, get_pv, timeSet, mqttErr
from dash_back.models import Post
import paho.mqtt.publish as publish
from datetime import datetime,tzinfo,timedelta
from datetime import date
import json

logger = get_task_logger(__name__)


# @shared_task()
# def task_save_latest_flickr_image():
#    """
#    Saves latest image from Flickr
#    """
#    save_latest_flickr_image()
#    logger.info("Saved image from Flickr")


# @periodic_task(run_every=crontab(minute="*/30"))
# def task_save_latest_flickr_image():
#    """
#    Saves latest image from Flickr
#    """
#    save_latest_flickr_image()
#    logger.info("Saved image from Flickr")

@shared_task()
def task_test():
    """
    test!!!
    """
    price_to_db()
    logger.info("test!!! abcdef")

@shared_task()
def task_schedule():
    """
    scheduleFlexi!!!
    """
    scheduled_flexi()
    logger.info("FLEXI")

@shared_task()
def task_exec_all():
    """
    Execute all requests
    """
    exec_all()
    logger.info("execute all")

@shared_task()
def task_hydro():
    get_hydro()
    logger.info("Hydro")
    
@shared_task()
def task_pv():
    get_pv()
    logger.info("PV")

@shared_task()
def task_setTime():
    timeSet()
    logger.info("TimeSet")
    
    
@shared_task()
def task_mqtt_error(dev,payload):
    #mqttErr(dev,payload)
    data_out = json.loads(payload.decode())
    timestamp = int(data_out['payload']['timestamp'])
    timestamp_iso = datetime.fromtimestamp(timestamp).isoformat()
    value = float(data_out['payload']['power'])    
    exist = Post.objects.filter(created_date=timestamp_iso,devId = dev)
    topic = dev + "/timestamp"
    if exist.count() == 1:
        jObj = {
            "time": timestamp,
            "pow": 0,
            }
        publish.single(topic, str(jObj), hostname="159.89.103.242", port=1883)
    else:
        Post.objects.create(devId=dev,value=value,created_date=timestamp_iso)
    logger.info("MQTT ERROR")
    

# @periodic_task(
#     run_every=(crontab(minute='*/2')),
#     name="task_test",
#     ignore_result=True
# )
# def task_test():
#     print("it works!")
#     logger.info("Woeks!!!")




# @periodic_task(
#     run_every=(crontab(minute='*/1440')),
#     name="task_empty_variants_table",
#     ignore_result=True
# )

# def task_empty_variants_table():
#     """
#     Emptying variants table every xxx min
#     """
#     emptying_variants_table()
#     logger.info("emtying variants")
