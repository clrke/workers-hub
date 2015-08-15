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
    message = models.TextField()


class Profession(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Request(models.Model):
    user = models.ForeignKey(User)
    professions = models.ManyToManyField(Profession)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    range_min = models.IntegerField()
    range_max = models.IntegerField()

    def __str__(self):
        return self.subject


class Image(models.Model):
    url = models.CharField(max_length=255)
    request = models.ForeignKey(Request)


class Proposal(models.Model):
    worker = models.ForeignKey(Worker)
    cost = models.IntegerField()
    message = models.TextField()
    status = models.CharField(max_length=255)
    request = models.ForeignKey(Request)

    def __str__(self):
        return self.request.subject

