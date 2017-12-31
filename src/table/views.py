from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render

from enum import Enum
import collections

from table.models import *
from ejudge.database import EjudgeDatabase, RunStatus
from ejudge.models import Contest
from . import models


def get_contest(user):
    for contest in models.VirtualContest.objects.all():
        if user.startswith(contest.login_prefix):
            return contest
    return contest


class CountryStatus:
    total = 0
    solved = 0
    country = None

    def __repr__(self):
        return str(self.__dict__)


@login_required
def index(request):
    user = request.user
    contest = get_contest(user.username)
    problem_statuses_by_user = load_from_ejudge_runs(request.user)
    problem_statuses = problem_statuses_by_user.get(user.info.ejudge_user_id, {})

    return render(request, 'table/table.html', get_result(contest, problem_statuses))


@login_required
def monitor(request):
    problem_statuses_by_user = load_from_ejudge_runs()
    contest = get_contest(request.user.username)
    monitor = []
    for user, problem_statuses in problem_statuses_by_user.items():
        user_result = get_result(contest, problem_statuses)
        monitor.append((user_result['score'], user_result['last_ok'], user, user_result))

    return render(request, 'table/monitor.html', {
        'monitor': sorted(monitor, key=lambda x: (-x[0], x[1])),
    })


def read_statement(request, problem_id):
    user = request.user
    contest = get_contest(user.username)
    problem_statuses_by_user = load_from_ejudge_runs(user)
    problem_statuses = problem_statuses_by_user.get(user.info.ejudge_user_id, {})
    user_result = get_result(contest, problem_statuses)
    cards = Card.objects.filter(ejudge_short_name=problem_id)
    if len(cards) != 1:
        return HttpResponseNotFound()
    card = cards[0]
    if not user_result['card_statuses'].get(card.id).available:
        return HttpResponseForbidden()

    statement_path = card.get_statement_path()
    with open(statement_path, 'rb') as statement_file:
        statement_content = statement_file.read()
        return HttpResponse(statement_content, content_type='application/pdf')


class CardStatus:
    problem_status = None
    card = None
    needs_str = None
    gives_str = None
    available = False


def get_result(contest, problem_statuses):
    cards = models.Card.objects.filter(contest=contest).all()

    inventory = collections.defaultdict(int)
    score = 0

    country_statuses = {}
    for country in models.Country.objects.all():
        country_status = CountryStatus()
        country_status.total = 0
        country_status.solved = 0
        country_status.country = country
        country_statuses[country.id] = country_status

    card_statuses = {}
    last_ok = 0
    for card in cards:
        card_status = card_statuses.setdefault(card.id, CardStatus())
        card_status.card = card
        card_status.problem_status = problem_statuses.setdefault(card.ejudge_short_name, ProblemStatus())

        country_status = country_statuses[card.country.id]
        country_status.total += 1

        if card_status.problem_status.state == ProblemState.SOLVED:
            add_to_dict(card.get_gives(), inventory)
            score += card.score
            country_status.solved += 1
            last_ok = max(last_ok, card_status.problem_status.time)
        card_status.needs_str = [cr.resource.name + '×' + str(cr.count) for cr in card.get_needs()]
        card_status.gives_str = [cr.resource.name + '×' + str(cr.count) for cr in card.get_gives()]

    for card_status in card_statuses.values():
        card_status.available = is_subset(create_dict(card_status.card.get_needs()), inventory)

    for country_status in country_statuses.values():
        if country_status.solved >= country_status.total:
            score += country_status.country.bonus

    card_statuses_by_level = [[] for i in range(6)]
    for card_status in card_statuses.values():
        card_statuses_by_level[card_status.card.level].append(card_status)

    resources = list(models.Resource.objects.all())

    return {
        'inventory': inventory,
        'score': score,
        'last_ok': last_ok,
        'card_statuses': card_statuses,
        'card_statuses_by_level': card_statuses_by_level,
        'country_statuses': country_statuses,
        'debug': country_statuses,
        'resources': resources,
        'ProblemState': ProblemState,
    }


def create_dict(card_resources):
    result = {}
    add_to_dict(card_resources, result)
    return result


def add_to_dict(card_resources, inventory):
    for cr in card_resources.all():
        inventory[cr.resource.id] = inventory.get(cr.resource.id, 0) + cr.count
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


ProblemState.do_not_call_in_templates = True


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
        problems = problems_by_user.setdefault(run.user_id, {})
        if run.problem_id not in contest.problems:
            continue
        short_name = contest.problems[run.problem_id].short_name
        problem_status = problems.setdefault(short_name, ProblemStatus())
        if run.status == RunStatus.OK:
            problem_status.state = ProblemState.SOLVED
            problem_status.time = run.time
        elif problem_status.state != ProblemState.SOLVED:
            problem_status.state = ProblemState.ATTEMPTED
            problem_status.time = run.time
    return problems_by_user
