# from celery.task.schedules import crontab # type: ignore
# from celery.decorators import periodic_task # type: ignore
from celery.utils.log import get_task_logger # type: ignore
from celery import shared_task #type: ignore

from dash_back.utils import test
#from photos.utils import emptying_variants_table

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
    test()
    logger.info("test!!!")


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
