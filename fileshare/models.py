from django.db import models
import uuid


class Folder(models.Model):
    name = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


def get_upload_path(instance, filename):
    return f"{instance.folder.name}/{filename}"


class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
