from django.contrib.auth.models import User
from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=255)
    approved = models.BooleanField()

    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.ForeignKey(User)
    professions = models.ManyToManyField(Profession, blank=True)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    mobile_number = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = models.ForeignKey(User)
    worker = models.ForeignKey(Worker)
    rating = models.SmallIntegerField()
    type = models.CharField(max_length=255)
    message = models.TextField()

    CUSTOMER_WORKER = 'CUSTOMER_WORKER'
    WORKER_CUSTOMER = 'WORKER_CUSTOMER'

    def __str__(self):
        if self.type == self.CUSTOMER_WORKER:
            return '[WORKER %d | %s] %s' % (self.rating, self.worker, self.message)
        elif self.type == self.WORKER_CUSTOMER:
            return '[CUSTOMER %d | %s] %s' % (self.rating, self.user, self.message)

        return self.type


class Request(models.Model):
    user = models.ForeignKey(User)
    professions = models.ManyToManyField(Profession)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    range_min = models.IntegerField()
    range_max = models.IntegerField()
    status = models.CharField(max_length=255)

    OPEN = 'OPEN'
    ACCEPTED = 'ACCEPTED'
    CLOSED = 'CLOSED'

    def __str__(self):
        return '[%s] %s' % (self.user.username, self.subject)

    def accepted_worker_id(self):
        accepted_workers = [proposal.worker_id for proposal in self.proposal_set.all() if proposal.status == Proposal.ACCEPTED]

        if len(accepted_workers):
            return str(accepted_workers[0])
        else:
            return ''


class Image(models.Model):
    url = models.CharField(max_length=255)
    request = models.ForeignKey(Request)

    def __str__(self):
        return self.request.subject


class Proposal(models.Model):
    worker = models.ForeignKey(Worker)
    cost = models.FloatField()
    message = models.TextField()
    status = models.CharField(max_length=255)
    request = models.ForeignKey(Request)

    OPEN = 'OPEN'
    ACCEPTED = 'ACCEPTED'

    def __str__(self):
        return '[%s] %s' % (self.request.subject, self.message)
