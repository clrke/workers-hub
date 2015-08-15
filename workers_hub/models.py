from django.contrib.auth.models import User
from django.db import models


class Worker(models.Model):
    user = models.ForeignKey(User)


class UserProfile(models.Model):
    mobile_number = models.CharField(max_length=255)
    user = models.ForeignKey(User)


class Review(models.Model):
    user = models.ForeignKey(User)
    worker = models.ForeignKey(Worker)
    type = models.CharField(max_length=255)


class Profession(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)


class Request(models.Model):
    user = models.ForeignKey(User)
    professions = models.ManyToManyField(Profession)
