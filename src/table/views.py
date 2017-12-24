from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from table.models import *
from enum import Enum

from ejudge.database import EjudgeDatabase, RunStatus
from ejudge.models import Contest
from . import models


class CardView:
    card = None
    problem_status = None

@login_required
def index(request):
    problems = load_from_ejudge_runs(request.user)

    cards = models.Card.objects.all()
    inventory = {}
    score = 0
    for card in cards:
        card.problem_status = problems.setdefault(card.ejudge_short_name, ProblemStatus())
        if card.problem_status.state == ProblemState.SOLVED:
            add_to_dict(card.gives, inventory)
            score += card.score

    for card in cards:
        card.available = is_subset(create_dict(card.needs), inventory)
        card.str = str(create_dict(card.needs)) + ' ' + str(inventory)
        
    return render(request, 'table/table.html', {
        'inventory': inventory,
        'score': score,
        'cards': cards,
        'debug': inventory,
    })

def create_dict(resources):
    result = {}
    add_to_dict(resources, result)
    return result

def add_to_dict(resources, inventory):
    for r in resources:
       inventory[r] = inventory.get(r, 0) + 1
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

@login_required
def initdb(request):
    Card.objects.all().delete()
    Card(ejudge_short_name="00", name="registration-newyear", needs="", gives="a", score=0).save()
    Card(ejudge_short_name="01", name="problem01", needs="", gives="b", score=1).save()
    Card(ejudge_short_name="02", name="problem02", needs="ab", gives="с", score=2).save()
    Card(ejudge_short_name="03", name="problem03", needs="aabbc", gives="с", score=5).save()
    return HttpResponse("Loaded.")

