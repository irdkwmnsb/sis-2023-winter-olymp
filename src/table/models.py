from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=255, help_text='Например, пушка')
    name_acc_one = models.CharField(max_length=255, help_text='Например, (одну) пушку')
    name_acc_two = models.CharField(max_length=255, help_text='Например, (две) пушки')
    name_acc_five = models.CharField(max_length=255, help_text='Например, (пять) пушек')
    color = models.CharField(max_length=10, help_text='blue, color, red или green')

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, help_text='Например, Германия')
    name_gen = models.CharField(max_length=255, help_text='Например, Германии')
    bonus = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Card(models.Model):
    ejudge_short_name = models.CharField(db_index=True, max_length=255)
    name = models.CharField(max_length=255, help_text='Имя карты/замка')
    needs = models.ManyToManyField(Resource, through='NeedsCardResource', related_name='needs+')
    gives = models.ManyToManyField(Resource, through='GivesCardResource', related_name='gives+')
    score = models.PositiveIntegerField()
    photo = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    country = models.ForeignKey(Country, related_name='cards')

    def get_statement_path(self):
        return "%s.pdf" % self.ejudge_short_name

    def get_needs(self):
        return NeedsCardResource.objects.filter(card=self).all()

    def get_gives(self):
        return GivesCardResource.objects.filter(card=self).all()


class VirtualContest(models.Model):
    login_prefix = models.CharField(max_length=255)
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
