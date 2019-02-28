from collections import defaultdict
from pathlib import Path
import re

odir=Path("param-test-odir")

score_d = {}
score_avg_d = defaultdict(list)

for lang_path in Path("data/local").glob("*"):
    lang = lang_path.name
    if len(str(lang)) != 3:
        continue

    for fn in (odir / lang).glob("*"):
        seq1_max = re.findall("s1m(\d+)", str(fn))[0]
        seq2_max = re.findall("s2m(\d+)", str(fn))[0]
        with open(str(fn)) as f:
            per = float(f.readlines()[0].split()[-1])
            score_d[(lang, int(seq1_max), int(seq2_max))] = per
            score_avg_d[(int(seq1_max), int(seq2_max))].append(per)
    print(lang)
    print("2,2:", score_d[(lang, 2, 2)])
    print("3,2:", score_d[(lang, 2, 3)])
    print("2,3:", score_d[(lang, 3, 2)])
    print("3,3:", score_d[(lang, 3, 2)])

for key in score_avg_d:
    print(key)
    print(sum(score_avg_d[key])/len(score_avg_d[key]))
