from celery import shared_task
from django.conf import settings
import os
import shutil

from shorturl.models import ShortUrl
from datetime import datetime, timedelta
from .models import Folder


@shared_task(bind=True)
def zip_files(self, name):
    try:
        os.chdir(settings.MEDIA_ROOT)  # change the working directory to the folder
        shutil.make_archive(base_name=f"{name}", format="zip", root_dir=f"{name}")
        shutil.rmtree(f"{name}")  # removed the folder cause not needed
    except:
        return False

    return True


# to delete a folder
@shared_task(bind=True)
def delete_folder(self, folder_name):
    try:  # folder is not created if first file is invalid, so exception might occur
        os.chdir(settings.MEDIA_ROOT)
        shutil.rmtree(f"{folder_name}")
    except:
        pass

    Folder.objects.filter(name=folder_name).delete()
    return True


# periodic task to delete fils older than 10 days
@shared_task(bind=True)
def delete_files(self):
    current = datetime.now()
    delta = timedelta(days=10)  # timedelta for 10days
    old = ShortUrl.objects.filter(date_created__lte=current - delta)
    os.chdir(settings.MEDIA_ROOT)  # change the working directory to the folder
    count = 0

    for o in old:
        try:
            name = o.link.split("/")[4]
            shutil.rmtree(name)
            count += 1
        except NotADirectoryError:
            os.remove(name)
            count += 1
        except:
            pass
        o.delete()

    return f"{count} Old folders deleted"
