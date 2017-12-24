from django.db import models
from django.contrib.auth import models as auth_models

import djchoices

class Card(models.Model):
    ejudge_short_name = models.CharField(db_index=True, max_length=255)
    name = models.CharField(max_length=255)
    needs = models.CharField(max_length=255) 
    gives = models.CharField(max_length=255) 
    score = models.PositiveIntegerField()

class CardStatusEnum(djchoices.DjangoChoices):
    CLOSED = djchoices.ChoiceItem(0, 'Closed')
    OPENED = djchoices.ChoiceItem(1, 'Opened')
    READ = djchoices.ChoiceItem(2, 'Read')
    TRIED = djchoices.ChoiceItem(3, 'Tried')
    SOLVED = djchoices.ChoiceItem(4, 'Solved')

class CardStatus(models.Model):
    card = models.ForeignKey(Card, related_name='statuses')

    user = models.ForeignKey(auth_models.User, related_name='card_statuses')

    status = models.PositiveIntegerField(
        choices=CardStatusEnum.choices,
        validators=[CardStatusEnum.validator],
        db_index=True
    )

    # WTF?
    class Meta:
        ordering = ['status']

    @classmethod
    def get_card_status(cls, card, user):
        qs = cls.objects.filter(card=card, user=user)
        if qs.exists():
            return qs.aggregate(models.Max('status'))['status__max']
        return CardStatusEnum.CLOSED
