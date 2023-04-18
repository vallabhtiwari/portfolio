from django.db import models

# Create your models here.


class Feedback(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    feedback = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
