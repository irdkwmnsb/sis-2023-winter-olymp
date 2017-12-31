from django.db import models
from enum import Enum


class Gender(Enum):
    MALE = 0
    FEMALE = 1
    NEUTER = 2


class Resource(models.Model):
    name = models.CharField(max_length=255, help_text='Например, пушка')
    name_acc_one = models.CharField(max_length=255, help_text='Например, (одну) пушку')
    name_acc_two = models.CharField(max_length=255, help_text='Например, (две) пушки')
    name_acc_five = models.CharField(max_length=255, help_text='Например, (пять) пушек')
    color = models.CharField(max_length=10, help_text='blue, yellow, red или green')
    gender = models.PositiveIntegerField(
        choices=[(Gender.MALE.value, 'Male'), (Gender.FEMALE.value, 'Female'), (Gender.NEUTER.value, 'Neuter')]
    )

    def __str__(self):
        return self.name

    def get_name_for_count(self, count):
        last = count % 10
        prelast = (count // 10) % 10
        if prelast != 1 and 2 <= last <= 4:
            return self.name_acc_two
        if 5 <= last <= 9 or last == 0:
            return self.name_acc_five
        if prelast == 1:
            return self.name_acc_five
        return self.name_acc_one


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
    
    def __str__(self):
        return '%s. %s' % (self.ejudge_short_name, self.name)

    def get_statement_path(self):
        return "%s.pdf" % self.ejudge_short_name

    def get_needs(self):
        return NeedsCardResource.objects.filter(card=self).all()

    def get_gives(self):
        return GivesCardResource.objects.filter(card=self).all()

    def _get_resources_description(self, resources):
        result = ''
        for idx, cr in enumerate(resources):
            result += ('%s %s' % (
                self._resource_count_to_string(cr.resource, cr.count), cr.resource.get_name_for_count(cr.count)
            )).strip()
            if idx < len(resources) - 2:
                result += ', '
            elif idx == len(resources) - 2:
                result += ' и '
        return result

    def get_needs_description(self):
        return self._get_resources_description(list(self.get_needs()))

    def get_gives_description(self):
        return self._get_resources_description(list(self.get_gives()))

    def _resource_count_to_string(self, resource, count):
        male_ints = {
            1: '',
            2: 'два',
            3: 'три',
            4: 'четыре',
            5: 'пять',
            6: 'шесть',
            7: 'семь',
            8: 'восемь',
            9: 'девять',
            10: 'десять',
        }
        female_ints = {
            # 1: 'одну',
            2: 'две',
        }
        neuter_ints = {
            # 1: 'одно',
        }
        if resource.gender == Gender.NEUTER.value and count in neuter_ints:
            return neuter_ints[count]
        if resource.gender == Gender.FEMALE.value and count in female_ints:
            return female_ints[count]
        if count in male_ints:
            return male_ints[count]
        return str(count)


class VirtualContest(models.Model):
    login_prefix = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    cards = models.ManyToManyField(Card, related_name='contest')

    def __str__(self):
        return self.name


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
