# from celery.task.schedules import crontab # type: ignore
# from celery.decorators import periodic_task # type: ignore
from celery.utils.log import get_task_logger # type: ignore
from celery import shared_task #type: ignore

from dash_back.utils import price_to_db, scheduled_flexi, exec_all, get_hydro, get_pv, timeSet, mqttErr, update_db_coeff
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
    #logger.info("test!!! abcdef")

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
    #logger.info("execute all")

@shared_task()
def task_hydro():
    get_hydro()
    #logger.info("Hydro")
    
@shared_task()
def task_pv():
    get_pv()
    #logger.info("PV")

@shared_task()
def task_setTime():
    timeSet()
    #logger.info("TimeSet")
    
    
@shared_task()
def task_mqtt_error(error_list):
    mqttErr(error_list)
    
    #logger.info("MQTT ERROR")

# @shared_task()
# def task_update_db():
#     update_db_coeff()
#     logger.info("COEFF")

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
