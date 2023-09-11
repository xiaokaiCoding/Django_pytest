from django.db import models

# Create your models here.
class UserApi(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.DecimalField(max_digits=12,decimal_places=0)