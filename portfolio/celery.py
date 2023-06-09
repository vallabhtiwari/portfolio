from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
app = Celery("portfolio")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")
app.config_from_object(settings, namespace="CELERY")

# celery beat settings
app.conf.beat_schedule = {
    "delete_files_older_than_10_days": {
        "task": "fileshare.tasks.delete_files",
        "schedule": crontab(minute=0, hour=0),
    },
    "delete_feedbacks_older_than_10_days": {
        "task": "base.tasks.delete_feedbacks",
        "schedule": crontab(minute=0, hour=1),
    },
}
#################
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
