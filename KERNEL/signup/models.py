from django.db import models

# Create your models here.
from django.db import models

class UserTable(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username