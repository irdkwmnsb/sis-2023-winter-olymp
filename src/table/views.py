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

    # TODO: fix
    contest = models.VirtualContest.objects.all()[0]
    cards = models.Card.objects.filter(contest=contest).all()

    inventory = {}
    score = 0

    countries = {}
    for country in models.Country.objects.all():
        countries[country.id] = country
        country.total = 0
        country.solved = 0

    for card in cards:
        card.problem_status = problems.setdefault(card.ejudge_short_name, ProblemStatus())
        country = countries[card.country.id]
        country.total += 1
        if card.problem_status.state == ProblemState.SOLVED:
            add_to_dict(card.get_gives(), inventory)
            score += card.score
            country.solved += 1
        card.needs_str = [cr.resource.name + '×' + str(cr.count) for cr in card.get_needs()]
        card.gives_str = [cr.resource.name + '×' + str(cr.count) for cr in card.get_gives()]

    for card in cards:
        card.available = is_subset(create_dict(card.get_needs()), inventory)
        card.str = str(create_dict(card.get_needs())) + ' ' + str(inventory)

    cards_by_level = [[] for i in range(6)]
    for card in cards:
        cards_by_level[card.level].append(card)
        
    return render(request, 'table/table.html', {
        'inventory': inventory,
        'score': score,
        'cards_by_level': cards_by_level,
        'countries': countries,
        'debug': inventory,
    })

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

def make_country(name):
    tmp = Country(name=name)
    tmp.save()
    return tmp

def make_card(**kwargs):
    card = Card(**kwargs)
    card.save()
    return card

def tmp():
    aaa = make_resource('aaa')
    bbb = make_resource('bbb')
    ccc = make_resource('ccc')


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

    card = make_card(ejudge_short_name="01", name="kek", score=0)
    GivesCardResource(card=card, resource=r0, count=1).save()

@login_required
def initdb(request):
    Resource.objects.all().delete()
    Card.objects.all().delete()
    Country.objects.all().delete()
    VirtualContest.objects.all().delete()
    NeedsCardResource.objects.all().delete()
    NeedsCardResource.objects.all().delete()
    c0 = VirtualContest(name='Contest 0')
    c0.save()
    r0 = make_resource('r0')
    r1 = make_resource('r1')
    r2 = make_resource('r2')
    r3 = make_resource('r3')
    gb = make_country('gb')
    de = make_country('de')
    ch = make_country('ch')
    cz = make_country('cz')
    ro = make_country('ro')
    it = make_country('it')
    fr = make_country('fr')


    card = make_card(ejudge_short_name="04", name="dessert-maker", score=0, level=1, country=cz)
    c0.cards.add(card)
    GivesCardResource(card=card, resource=r2, count=1).save()

    card = make_card(ejudge_short_name="12", name="hamming", score=0, level=1, country=ch)
    c0.cards.add(card)
    GivesCardResource(card=card, resource=r0, count=1).save()
    GivesCardResource(card=card, resource=r2, count=1).save()

    card = make_card(ejudge_short_name="02", name="third-buy-discount", score=0, level=1, country=fr)
    c0.cards.add(card)
    GivesCardResource(card=card, resource=r0, count=1).save()

    card = make_card(ejudge_short_name="03", name="digital-display", score=1, level=1, country=fr)
    c0.cards.add(card)
    GivesCardResource(card=card, resource=r1, count=1).save()

    card = make_card(ejudge_short_name="01", name="kek", score=0, level=1, country=de)
    c0.cards.add(card)
    GivesCardResource(card=card, resource=r0, count=1).save()

    card = make_card(ejudge_short_name="05", name="straight-array", score=1, level=1, country=de)
    c0.cards.add(card)
    GivesCardResource(card=card, resource=r1, count=1).save()
    GivesCardResource(card=card, resource=r2, count=1).save()

    card = make_card(ejudge_short_name="07", name="palindr", score=1, level=2, country=gb)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r0, count=1).save()
    NeedsCardResource(card=card, resource=r2, count=1).save()

    card = make_card(ejudge_short_name="06", name="word-math", score=1, level=2, country=ch)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r0, count=1).save()
    NeedsCardResource(card=card, resource=r1, count=1).save()

    card = make_card(ejudge_short_name="09", name="gentest", score=1, level=2, country=cz)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r0, count=1).save()
    NeedsCardResource(card=card, resource=r1, count=1).save()
    NeedsCardResource(card=card, resource=r2, count=1).save()

    card = make_card(ejudge_short_name="11", name="crosses", score=2, level=2, country=fr)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r2, count=2).save()

    card = make_card(ejudge_short_name="10", name="good-and-bad-postmen", score=2, level=2, country=de)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r1, count=1).save()

    card = make_card(ejudge_short_name="08", name="string-io", score=2, level=2, country=it)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r0, count=2).save()

    card = make_card(ejudge_short_name="31", name="highway", score=2, level=2, country=it)
    c0.cards.add(card)
    NeedsCardResource(card=card, resource=r0, count=1).save()
    NeedsCardResource(card=card, resource=r1, count=1).save()
    NeedsCardResource(card=card, resource=r2, count=1).save()

    card = make_card(ejudge_short_name="13", name="governor", score=0, level=3, country=gb)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="28", name="divisibility", score=0, level=3, country=gb)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="27", name="distinct-dice", score=0, level=3, country=ro)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="21", name="anti", score=0, level=3, country=ro)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="19", name="substring", score=0, level=3, country=de)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="26", name="rube-goldberg", score=0, level=3, country=fr)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="20", name="hol", score=0, level=3, country=it)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="25", name="twohoses", score=0, level=3, country=it)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="23", name="queen", score=0, level=4, country=gb)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="30", name="warehouse-job", score=0, level=4, country=gb)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="14", name="theorem", score=0, level=4, country=ro)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="17", name="lateagain", score=0, level=4, country=ro)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="15", name="epig", score=0, level=4, country=cz)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="24", name="protect", score=0, level=4, country=cz)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="16", name="trenches", score=0, level=4, country=cz)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="29", name="pending-tasks", score=0, level=4, country=ch)
    c0.cards.add(card)

    card = make_card(ejudge_short_name="18", name="ineq", score=0, level=4, country=ch)
    c0.cards.add(card)

    c0.save()
    return HttpResponse("Loaded.")
