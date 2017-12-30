from django.db import models
from django.contrib.auth import models as auth_models

import djchoices

class Resource(models.Model):
    name = models.CharField(max_length=255)

class Country(models.Model):
    name = models.CharField(max_length=255)
    bonus = models.PositiveIntegerField()
    
class Card(models.Model):
    ejudge_short_name = models.CharField(db_index=True, max_length=255)
    name = models.CharField(max_length=255)
    needs = models.ManyToManyField(Resource, through='NeedsCardResource', related_name='needs+')
    gives = models.ManyToManyField(Resource, through='GivesCardResource', related_name='gives+')
    score = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    country = models.ForeignKey(Country, related_name='cards')

    def get_statement_path(self):
        return "%s.pdf" % self.ejudge_short_name

    def get_needs(self):
      return NeedsCardResource.objects.filter(card=self).all()

    def get_gives(self):
      return GivesCardResource.objects.filter(card=self).all()

class VirtualContest(models.Model):
    login_regex = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    cards = models.ManyToManyField(Card, related_name='contest')

class AbstractCardResource(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        abstract = True

class NeedsCardResource(AbstractCardResource):
    class Meta:
         unique_together = ('card', 'resource')

class GivesCardResource(AbstractCardResource):
    class Meta:
         unique_together = ('card', 'resource')
