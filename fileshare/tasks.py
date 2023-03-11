from celery import shared_task
from django.conf import settings
import os
import shutil

from shorturl.models import ShortUrl
from datetime import datetime, timedelta


@shared_task(bind=True)
def zip_files(self, name):
    os.chdir(settings.MEDIA_ROOT)  # change the working directory to the folder
    shutil.make_archive(base_name=f"{name}", format="zip", root_dir=f"{name}")
    shutil.rmtree(f"{name}")  # removed the folder cause not needed

    return "Folder zipped"


@shared_task(bind=True)
def delete_files(self):
    current = datetime.now()
    delta = timedelta(days=10)
    old = ShortUrl.objects.filter(date_created__lte=current - delta)
    os.chdir(settings.MEDIA_ROOT)  # change the working directory to the folder
    count = 0

    for o in old:
        name = o.link.split("/")[4]
        try:
            shutil.rmtree(name)
            count += 1
        except NotADirectoryError:
            os.remove(name)
            count += 1
        except:
            pass
        o.delete()

    return f"{count} Old files deleted"
