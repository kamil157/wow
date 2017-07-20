import os

import requests

from simc import wowapi

# This script is used to generate words used for the talent abbreviations
from wow import settings


def get_talent_names():
    return [talent['spell']['name']
            for wow_class in wowapi.get_talents().values()
            for row in wow_class['talents']
            for column in row
            for talent in column]


r = requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt')
# Check only words that are long enough to make sense
english_dictionary = set(word.strip() for word in r.text.split() if len(word.strip()) >= 3)

# Created manually by checking the output produced by this script
with open(os.path.join(settings.BASE_DIR, 'simc', 'tools', 'talents', 'bad')) as f:
    bad = set(x.strip() for x in f.readlines())

with open(os.path.join(settings.BASE_DIR, 'simc', 'tools', 'talents', 'good')) as f:
    good = set(x.strip() for x in f.readlines())


def get_short_talent_name_v1(talent_name):
    words = talent_name.split()
    if len(words) == 1:
        return talent_name[:3]
    return ''.join(w[0] for w in words)


def get_short_talent_name_v2(talent_name):
    words = talent_name.split()
    if len(words) == 1:
        for i in range(1, len(talent_name)):
            left, right = talent_name[:i], talent_name[i:]
            if left.lower() in english_dictionary and right.lower() in english_dictionary:
                return left[0].upper() + right[0].upper(), left, right
    return get_short_talent_name_v1(talent_name), None, None


results = []
for name in get_talent_names():
    v1 = get_short_talent_name_v1(name)
    v2, left, right = get_short_talent_name_v2(name)
    if v1 != v2:
        score = 0 if name in bad else 1 if name in good else -1
        s = ('{} {} {:<15} {} {} {:>10} {:<10}'.format(score, name.lower() in english_dictionary, name, v1, v2, left,
                                                       right.title()))
        results.append(s)

for s in sorted(set(results)):
    print(s)
