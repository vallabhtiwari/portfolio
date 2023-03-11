from django.db import models
import shortuuid
from datetime import datetime

# Create your models here
url_ids = set()


class ShortUrl(models.Model):
    link = models.URLField(max_length=1000)
    id = models.CharField(max_length=4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        id = shortuuid.ShortUUID().random(length=4)
        while id in url_ids:
            id = shortuuid.ShortUUID().random(length=4)

        self.id = id
        url_ids.add(self.id)
        super(ShortUrl, self).save(*args, **kwargs)
