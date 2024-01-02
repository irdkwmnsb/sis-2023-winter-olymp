import itertools
COUNTRIES = itertools.cycle(["ur", "zb", "pb", "kk", "pm", "bl", "mo"])
with open("polygon-contest/contest.xml") as f:
    content = f.read()
    l = content.split("<problems>")[-1].split("</problems>")[0].strip()
    for i, line in enumerate(l.split("\n")):
        line = line.strip()
        index = line.split('index="')[-1].split('"')[0]
        shortname = line.split('"/>')[0].split('/')[-1]
        level = 1
        needs_junior = "0000"
        gives_junior = "1111"
        score_junior = "5"
        needs_adult = "0000"
        gives_adult = "1111"
        score_adult = "5"
        polygon_short_name = shortname
        print(i + 1, next(COUNTRIES), i + 1, shortname, level,
                            needs_junior, gives_junior, score_junior,
                            needs_adult, gives_adult, score_adult, polygon_short_name,
        sep='\t')