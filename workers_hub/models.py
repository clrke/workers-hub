from django.contrib.auth.models import User
from django.db import models


class Worker(models.Model):
    pass


class UserProfile(models.Model):
    mobile_number = models.CharField(max_length=255)
    user = models.ForeignKey(User)
