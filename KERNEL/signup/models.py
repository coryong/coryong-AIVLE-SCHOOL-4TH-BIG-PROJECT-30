from django.db import models

# Create your models here.
from django.db import models

class UserTable(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    area = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.username