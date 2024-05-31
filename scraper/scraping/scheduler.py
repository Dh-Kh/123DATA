from celery import Celery
from celery.signals import after_setup_logger
from celery.schedules import crontab
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders import scraping_spider
from datetime import datetime
import os
import logging

#issue with celery
#docker-compose run scrapy works

settings = get_project_settings()

app = Celery("tasks", broker=settings.get("REDIS_URL"))

logger = logging.getLogger(__name__)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    settings = get_project_settings()
    log_dir = settings.get("LOGS_DIR")
    log_file = os.path.join(log_dir, 'celery.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    #celery -A scheduler worker -l info --logfile=logs/celery.log
    
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour="0"), scrapy_scheduler.s(), name="scheduler")
    sender.add_periodic_task(crontab(minute=0, hour="12"), dump_task.s(), name="dump")
    sender.add_periodic_task(crontab(minute="*"), print_text.s(), name="print")

@app.task
def scrapy_scheduler():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(scraping_spider)
    process.start()
    logger.info("Scrapping task executed")
    
@app.task
def dump_task():
    settings = get_project_settings()
    db_host = settings.get("DB_HOST")
    db_user = settings.get("DB_USER")
    db_name = settings.get("DB_NAME")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_folder = os.path.join(script_dir, "dumps")
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    backup_file = db_name + "_" + timestamp + ".sql"
    os.makedirs(backup_folder, exist_ok=True)
    backup_cmd = "pg_dump -h {0} -U {1} -d {2} > {3}".format(db_host, db_user, db_name, os.path.join(backup_folder, backup_file))
    os.system(backup_cmd)
    logger.info("Dump task executed")
    
@app.task
def print_text():
    logger.info(f"[{datetime.now()}] Hello from Celery task!")