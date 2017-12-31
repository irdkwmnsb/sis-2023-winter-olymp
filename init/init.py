import json


INIT_FILE = 'init.txt'


def get_problem_name(polygon_shortname):
#    filename = 'polygon-contest/problems/%s/statements/russian/problem-properties.json' % polygon_shortname
#    with open(filename, encoding='utf-8') as f:
#        content = f.read()
#    parsed = json.loads(content) 
#    return parsed['name']
    return polygon_shortname

min_row = -4
max_row = 4
min_column = -5
HEADER =\
"""
from table.models import *

def make_resource(**kwargs):
    tmp = Resource(**kwargs)
    tmp.save()
    return tmp

def make_country(**kwargs):
    tmp = Country(**kwargs)
    tmp.save()
    return tmp

def make_card(**kwargs):
    tmp = Card(**kwargs)
    tmp.save()
    return tmp

Resource.objects.all().delete()
Card.objects.all().delete()
Country.objects.all().delete()
VirtualContest.objects.all().delete()
NeedsCardResource.objects.all().delete()
NeedsCardResource.objects.all().delete()
c_junior = VirtualContest(id=1, name="Олимпиада B'-C-C'", login_prefix="sis-2017-4")
c_junior.save()
c_adult = VirtualContest(id=2, name="Олимпиада A-A'-B", login_prefix="sis-2017-5")
c_adult.save()
r0 = make_resource(id=1,name='пушка',name_acc_one='пушку',name_acc_two='пушки',name_acc_five='пушек', color='green')
r1 = make_resource(id=2,name='катапульта',name_acc_one='катапульту',name_acc_two='катапульты',name_acc_five='катапульт', color='yellow')
r2 = make_resource(id=3,name='меч',name_acc_one='меч',name_acc_two='меча',name_acc_five='мечей', color='blue')
r3 = make_resource(id=4,name='ружьё',name_acc_one='ружьё',name_acc_two='ружья',name_acc_five='ружей', color='red')

gb = make_country(id=1, name='Великобритания', name_gen='Великобритании', bonus=5)
de = make_country(id=2, name='Германия', name_gen='Германии', bonus=5)
ch = make_country(id=3, name='Швейцария', name_gen='Швейцарии', bonus=5)
cz = make_country(id=4, name='Чехия', name_gen='Чехии', bonus=5)
ro = make_country(id=5, name='Румыния', name_gen='Румынии', bonus=5)
it = make_country(id=6, name='Италия', name_gen='Италии', bonus=5)
fr = make_country(id=7, name='Франция', name_gen='Франции', bonus=5)
"""


with open('init_script.py', 'w', encoding='utf-8') as output_file:
    print(HEADER, file=output_file)
    
    with open(INIT_FILE, 'r', encoding='utf-8') as init:
        for line in init:
            if not line.strip():
                continue
            line = line.strip().split('\t')
            # gb    07  palindr 2   1010    2201    2   0000    0010    1
            (photo, country, polygon_id, polygon_shortname, level_src,
                            needs_junior, gives_junior, score_junior,
                            needs_adult, gives_adult, score_adult)= line[:11]
            for contest, level, needs, gives, score in [
                            ('c_junior', int(level_src), needs_junior, gives_junior, score_junior),
                            ('c_adult', int(level_src) - 1, needs_adult, gives_adult, score_adult)]:
                if needs == 'xxxx':
                    continue
                print('card = make_card(ejudge_short_name="%s", name="%s", score=%d, level=%d, country=%s, photo=%d)' % (
                            polygon_id, polygon_shortname, int(score), level, country, int(photo)), file=output_file)
                print('%s.cards.add(card)' % (contest), file=output_file);
                for i in range(0, len(needs)):
                    cnt = int(needs[i])
                    if cnt > 0:
                        print ('NeedsCardResource(card=card, resource=r%d, count=%d).save()' % (i, cnt), file=output_file)
                for i in range(0, len(gives)):
                    cnt = int(gives[i])
                    if cnt > 0:
                        print ('GivesCardResource(card=card, resource=r%d, count=%d).save()' % (i, cnt), file=output_file)
                print ('', file=output_file)
        print ('c_junior.save()', file=output_file)
        print ('c_adult.save()', file=output_file)
