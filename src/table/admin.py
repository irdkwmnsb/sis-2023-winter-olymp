from django.contrib import admin
from . import models


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'ejudge_short_name', 'name', 'country')


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'gender')


@admin.register(models.VirtualContest)
class VirtualContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'login_prefix')