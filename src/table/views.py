from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from table.models import *
from enum import Enum

from ejudge.database import EjudgeDatabase, RunStatus
from ejudge.models import Contest
from . import models



def get_contest(user):
    # TODO: fix
    return models.VirtualContest.objects.all()[0]

class CountryStatus:
    total = 0
    solved = 0
    country = None

    def __repr__(self):
        return str(self.__dict__)


@login_required
def index(request):
    user = request.user
    problem_statuses_by_user = load_from_ejudge_runs(request.user)
    print('psby', problem_statuses_by_user)
    problem_statuses = problem_statuses_by_user.get(user.info.ejudge_user_id, {})
    print('ps', problem_statuses)

    return render(request, 'table/table.html', get_user_result(user, problem_statuses))

@login_required
def monitor(request):
    problem_statuses_by_user = load_from_ejudge_runs()
    print(problem_statuses_by_user)
    monitor = []
    for user, problem_statuses in problem_statuses_by_user.items():
        print(problem_statuses)
        user_result = get_user_result(user, problem_statuses)
        monitor.append((user_result['score'], user, user_result))

    return render(request, 'table/monitor.html', {
                    'monitor': sorted(monitor, reverse=True),
                    })   


def get_user_result(user, problem_statuses):
    contest = get_contest(user)
    cards = models.Card.objects.filter(contest=contest).all()

    inventory = {}
    score = 0

    country_statuses = {}
    for country in models.Country.objects.all():
        country_status = CountryStatus()
        country_status.total = 0
        country_status.solved = 0
        country_status.country = country
        country_statuses[country.id] = country_status

    for card in cards:
        print (problem_statuses)
        card.problem_status = problem_statuses.setdefault(card.ejudge_short_name, ProblemStatus())
        country_status = country_statuses[card.country.id]
        country_status.total += 1
        if card.problem_status.state == ProblemState.SOLVED:
            add_to_dict(card.get_gives(), inventory)
            score += card.score
            country_status.solved += 1
        card.needs_str = [cr.resource.name + '×' + str(cr.count) for cr in card.get_needs()]
        card.gives_str = [cr.resource.name + '×' + str(cr.count) for cr in card.get_gives()]

    for card in cards:
        card.available = is_subset(create_dict(card.get_needs()), inventory)
        card.str = str(create_dict(card.get_needs())) + ' ' + str(inventory)

    for country_status in country_statuses.values():
        if country_status.solved >= country_status.total:
            score += country_status.country.bonus

    cards_by_level = [[] for i in range(6)]
    for card in cards:
        cards_by_level[card.level].append(card)
        
    return {
        'inventory': inventory,
        'score': score,
        'cards_by_level': cards_by_level,
        'country_statuses': country_statuses,
        'debug': country_statuses,
    }

def create_dict(card_resources):
    result = {}
    add_to_dict(card_resources, result)
    return result

def add_to_dict(card_resources, inventory):
    for cr in card_resources.all():
       inventory[cr.resource.name] = inventory.get(cr.resource.name, 0) + cr.count
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

def load_from_ejudge_runs(user=None):
    contest = Contest(settings.EJUDGE_SERVE_CFG)
    ejudge_database = EjudgeDatabase()
    problems_by_user = {}

    if user:
        runs = ejudge_database.get_runs_by_user(user)
    else:
        runs = ejudge_database.get_runs()

    for run in runs:
        if run.status == RunStatus.IGNORED:
            continue
        print(run.user_id)
        problems = problems_by_user.setdefault(run.user_id, {})
        print (problems)
        short_name = contest.problems[run.problem_id].short_name
        problem_status = problems.setdefault(short_name, ProblemStatus())
        if run.status == RunStatus.OK:
            problem_status.state = ProblemState.SOLVED
            problem_status.time = run.time
        elif problem_status.state != ProblemState.SOLVED:
            problem_status.state = ProblemState.ATTEMPTED 
            problem_status.time = run.time
    return problems_by_user
