from django.db import models
from django.contrib.auth import models as auth_models

import djchoices

class Card(models.Model):
    ejudge_short_name = models.CharField(db_index=True, max_length=255)
    name = models.CharField(max_length=255)
    needs = models.CharField(max_length=255) 
    gives = models.CharField(max_length=255) 
    score = models.PositiveIntegerField()

