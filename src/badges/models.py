from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from models3d.models import Model

class BadgeManager(models.Manager):
    # Display only active badges
    def get_queryset(self):
        return super(BadgeManager, self).get_queryset().filter(active_on__lte=datetime.now()).defer('active_on')

class Badge(models.Model):
    objects = BadgeManager()
    user = models.OneToOneField(User)
    active_on = models.DateTimeField(default=datetime.now)

    class Meta:
        abstract = True

class Star(Badge):
    model = models.ForeignKey(Model)

    class Meta:
        unique_together = ('user', 'model')

class Collector(Badge):
    pass

class Pioneer(Badge):
    pass
