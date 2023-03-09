from celery import shared_task
from django.conf import settings
import os
import shutil


@shared_task(bind=True, name="tasks.zip_files")
def zip_files(self, name):
    os.chdir(settings.MEDIA_ROOT)  # change the working directory to the folder
    shutil.make_archive(base_name=f"{name}", format="zip", root_dir=f"{name}")
    shutil.rmtree(f"{name}")  # removed the folder cause not needed

    return "Folder zipped"
