from django.db import models
import uuid
from django.conf import settings
import os
import shutil


class Folder(models.Model):
    name = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def zip_files(self):
        os.chdir(settings.MEDIA_ROOT)
        shutil.make_archive(
            base_name=f"{self.name}", format="zip", root_dir=f"{self.name}"
        )

        shutil.rmtree(f"{self.name}")
        self.zipped = True


def get_upload_path(instance, filename):
    return f"{instance.folder.name}/{filename}"


class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
