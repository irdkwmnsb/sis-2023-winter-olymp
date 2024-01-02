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
import django
django.setup()
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
c_junior_test = VirtualContest(id=3, name="Младшая зимняя олимпиада (ТЕСТ)", login_prefix="sis-2023-0junior")
c_junior_test.save()
c_adult_test = VirtualContest(id=4, name="Старшая зимняя олимпиада (ТЕСТ)", login_prefix="sis-2023-0adult")
c_adult_test.save()
c_junior = VirtualContest(id=1, name="Младшая зимняя олимпиада", login_prefix="sis-2023-w-jun")
c_junior.save()
c_adult = VirtualContest(id=2, name="Старшая зимняя олимпиада", login_prefix="sis-2023-w-sen")
c_adult.save()
r0 = make_resource(id=1,name='поток',name_acc_one='поток',name_acc_two='потока',name_acc_five='потоков', color='green', gender=Gender.MALE.value)
r1 = make_resource(id=2,name='ссылка',name_acc_one='ссылку',name_acc_two='ссылки',name_acc_five='ссылок', color='yellow', gender=Gender.FEMALE.value)
r2 = make_resource(id=3,name='указатель',name_acc_one='указатель',name_acc_two='указателя',name_acc_five='указателей', color='blue', gender=Gender.MALE.value)
r3 = make_resource(id=4,name='вода',name_acc_one='воду',name_acc_two='воды',name_acc_five='воды', color='red', gender=Gender.FEMALE.value)

no = make_country(id=1, name='Русь', name_gen='Руси', bonus=5)
# Челябинская операция
# Битва за Каменск-Уральский
# Холмистая засада
# Долина Демидовская
# Судьбоносный поход в Нижний Тагил
# Пермский рубеж
zb = make_country(id=2, name='Забайкалье', name_gen='Забайкалья', bonus=5)
# Битва за Забайкальск
# Хилокский перевал
# Борьба за Улан-Удэ
# Тункинская долина
# Байкальский фронт
pb = make_country(id=3, name='Прибайкалье', name_gen='Прибайкалья', bonus=5)
# Битва на мысе Лисий
# Схватка у подножия хребта Каменск
# Борьба за поселок Хужир
# Решающее столкновение в Северобайкальске
# Прибайкальский фронт
kk = make_country(id=4, name='Кавказ', name_gen='Кавказа', bonus=5)
# Хребет Бештау
# Битва за Эльбрус
# Долина реки Терек
# Страстная Долина
# Крепость Хашури
pm = make_country(id=5, name='Примосковье', name_gen='Примосковья', bonus=5)
# Битва у подножия горы Лисья
# Тверская стенка
# Борьба за Чёрное озеро
# Коломенская крепость
# Подмосковный фронт
bl = make_country(id=6, name='Прибалтика', name_gen='Прибалтики', bonus=5)
# Сражение у побережья Лиепаи
# Захват Яунгшилы
# Битва за Куршскую косу
# Нацеленность на Нарву
# Балтийский фронт
mo = make_country(id=7, name='Луна', name_gen='Луны', bonus=5)
# Море Тишини
# Кратер Хармонии
# Долина Рассвета
# Гора Аристарх
# Лунное ущелье
"""


with open('init_script.py', 'w', encoding='utf-8') as output_file:
    print(HEADER, file=output_file)
    
    with open(INIT_FILE, 'r', encoding='utf-8') as init:
        for line in init:
            if not line.strip():
                continue
            line = line.strip().split('\t')
            # gb    07  palindr 2   1010    2201    2   0000    0010    1
            (photo, country, polygon_id, name, level_src,
                            needs_junior, gives_junior, score_junior,
                            needs_adult, gives_adult, score_adult, polygon_short_name)= line[:12]
            for contest, level, needs, gives, score in [
                            ('c_junior', int(level_src), needs_junior, gives_junior, score_junior),
                            ('c_junior_test', int(level_src), needs_junior, gives_junior, score_junior),
                            ('c_adult', int(level_src) - 1, needs_adult, gives_adult, score_adult),
                            ('c_adult_test', int(level_src) - 1, needs_adult, gives_adult, score_adult)]:
                if needs == 'xxxx':
                    continue
                print('card = make_card(ejudge_short_name="%s", name="%s", score=%d, level=%d, country=%s, photo=%d, polygon_short_name="%s")' % (
                            polygon_id, name, int(score), level, country, int(photo), polygon_short_name), file=output_file)
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
        print ('c_junior_test.save()', file=output_file)
        print ('c_adult.save()', file=output_file)
        print ('c_adult_test.save()', file=output_file)
