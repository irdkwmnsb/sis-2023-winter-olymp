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


with open('init_script.py', 'w', encoding='utf-8') as output_file:
#    print('from table.models import *', file=output_file)
#    print('AbstractTile.objects.all().delete()', file=output_file)
    
    with open(INIT_FILE, 'r', encoding='utf-8') as init:
        for line in init:
            if not line.strip():
                continue
            line = line.strip().split()
            print(line)
            # 01 kek 1 0000 1000 0
            polygon_id, polygon_shortname, level, needs, gives, score = line[:6]

            print('    card = make_card(ejudge_short_name="%s", name="%s", score=%d, level=%d)' % (
                            polygon_id, polygon_shortname, int(score), int(level)), file=output_file)
            for i in range(0, len(needs)):
                cnt = int(needs[i])
                if cnt > 0:
                    print ('    NeedsCardResource(card=card, resource=r%d, count=%d).save()' % (i, cnt), file=output_file)
            for i in range(0, len(gives)):
                cnt = int(gives[i])
                if cnt > 0:
                    print ('    GivesCardResource(card=card, resource=r%d, count=%d).save()' % (i, cnt), file=output_file)
            print ('', file=output_file)
        print ('    return HttpResponse("Loaded.")', file=output_file)

    
#            parameters = 'row=%d, column=%d, ejudge_short_name="%02d", name="%s", statement_file_name="%02d.pdf", automatic_open_time=%d' % \
#                (int(row), int(column), int(polygon_id), get_problem_name(polygon_shortname), int(polygon_id), int(open_time)) 
#    
#            if bonus == '':
#                parameters += ', solved_award=%d, wrong_penalty=%d' % (int(award), int(award) // 20)
#
#            print('%s(%s).save()' % (class_name, parameters), file=output_file)
