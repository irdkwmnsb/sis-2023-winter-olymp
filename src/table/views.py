from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from table.models import *
from enum import Enum

from ejudge.database import EjudgeDatabase, RunStatus
from ejudge.models import Contest
from . import models

@login_required
def index(request):
    problems = load_from_ejudge_runs(request.user)

    cards = models.Card.objects.all()
    inventory = {}
    score = 0
    for card in cards:
        card.problem_status = problems.setdefault(card.ejudge_short_name, ProblemStatus())
        if card.problem_status.state == ProblemState.SOLVED:
            add_to_dict(card.get_gives(), inventory)
            score += card.score
        card.needs_str = [ncr.resource.name + '×' + str(ncr.count) for ncr in card.get_needs()]
        card.gives_str = [ncr.resource.name + '×' + str(ncr.count) for ncr in card.get_gives()]

    for card in cards:
        card.available = is_subset(create_dict(card.get_needs()), inventory)
        card.str = str(create_dict(card.get_needs())) + ' ' + str(inventory)
        
    return render(request, 'table/table.html', {
        'inventory': inventory,
        'score': score,
        'cards': cards,
        'debug': inventory,
    })

def create_dict(card_resources):
    result = {}
    add_to_dict(card_resources, result)
    return result

def add_to_dict(card_resources, inventory):
    for r in card_resources.all():
       inventory[r.resource.name] = inventory.get(r.resource.name, 0) + r.count
    return inventory

def is_subset(requirements, inventory):
    for resource, needs in requirements.items():
        if needs > inventory.get(resource, 0):
            return False
    return True


class ProblemState(Enum):
    NOT_ATTEMPTED = 0
    ATTEMPTED = 1
    SOLVED = 2

class ProblemStatus:
    state = ProblemState.NOT_ATTEMPTED
    time = 0

    def __repr__(self):
        return str(self.__dict__)

def load_from_ejudge_runs(user):
    contest = Contest(settings.EJUDGE_SERVE_CFG)
    ejudge_database = EjudgeDatabase()
    problems = {}
    for run in ejudge_database.get_runs_by_user(user):
        if run.status == RunStatus.IGNORED:
            continue
        short_name = contest.problems[run.problem_id].short_name

        problem_status = problems.setdefault(short_name, ProblemStatus())
        if run.status == RunStatus.OK:
            problem_status.state = ProblemState.SOLVED
            problem_status.time = run.time
        elif problem_status.state != ProblemState.SOLVED:
            problem_status.state = ProblemState.ATTEMPTED 
            problem_status.time = run.time
    return problems


def make_resource(name):
    resource = Resource(name=name)
    resource.save()
    return resource

def make_card(**kwargs):
    card = Card(**kwargs)
    card.save()
    return card

@login_required
def initdb(request):
    Resource.objects.all().delete()
    aaa = make_resource('aaa')
    bbb = make_resource('bbb')
    ccc = make_resource('ccc')
    Card.objects.all().delete()

    c00 = make_card(ejudge_short_name="00", name="registration-newyear", score=0)
    GivesCardResource(card=c00, resource=aaa, count=1).save()

    c01 = make_card(ejudge_short_name="01", name="problem01", score=1)
    GivesCardResource(card=c01, resource=bbb, count=1).save()

    c02 = make_card(ejudge_short_name="02", name="problem02", score=2)
    NeedsCardResource(card=c02, resource=aaa, count=1).save()
    NeedsCardResource(card=c02, resource=bbb, count=1).save()
    GivesCardResource(card=c02, resource=ccc, count=1).save()

    c03 = make_card(ejudge_short_name="03", name="problem03", score=5)
    NeedsCardResource(card=c03, resource=aaa, count=2).save()
    NeedsCardResource(card=c03, resource=bbb, count=2).save()
    NeedsCardResource(card=c03, resource=ccc, count=1).save()
    GivesCardResource(card=c03, resource=ccc, count=1).save()
    return HttpResponse("Loaded.")

