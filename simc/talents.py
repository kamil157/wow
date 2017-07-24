import os
from functools import lru_cache
from itertools import product

from wow import settings

# In SimulationCraft, 0 means no talent selected
NO_TALENT = '0'


def get_talent_for_spec(spec_name, talent):
    try:
        spec_talent = next(t for t in talent if 'spec' in t and t['spec']['name'] == spec_name)
    except StopIteration:
        # If there is no spec info, this talent is for all specs which don't have a talent specified.
        spec_talent = next(t for t in talent if 'spec' not in t)
    return spec_talent['spell']


@lru_cache(maxsize=1)
def get_dictionary():
    with open(os.path.join(settings.BASE_DIR, 'simc/dictionary.txt')) as f:
        return set(word.strip() for word in f.readlines())


@lru_cache()
def get_short_talent_name(talent_name):
    words = talent_name.split()
    if len(words) == 1:
        dictionary = get_dictionary()

        # Check if the word can be made from two words
        for i in range(1, len(talent_name)):
            left, right = talent_name[:i], talent_name[i:]
            if left.lower() in dictionary and right.lower() in dictionary:
                return left[0].upper() + right[0].upper()
        return talent_name[:3]
    else:
        return ''.join(w[0] for w in words)


def get_configuration_name(configuration, spec_name, talent_info):
    talent_names = []
    for row, column_choice in enumerate(configuration):
        if column_choice != NO_TALENT:
            talent = talent_info[row][int(column_choice) - 1]
            talent_name = get_talent_for_spec(spec_name, talent)['name']
            talent_names.append(get_short_talent_name(talent_name))
    return ' '.join(talent_names)


def get_configurations(choice, talent_info, spec_name):
    # TODO annotate types
    values = [c if c else [NO_TALENT] for c in choice.values()]
    talents = product(*values)
    talent_str = [''.join(talent_choice) for talent_choice in talents]

    # E.g.:
    # copy=PM Shi MI AF FS LB Kin
    # talents=1111111
    copy = ('copy="{name}"\n'
            'talents={configuration}\n')

    # E.g.: profileset."PM Shi MI AF FS LB Kin"=talents=1111111
    profileset = 'profileset."{name}"=talents={configuration}'

    return make_output(spec_name, talent_info, talent_str, copy), \
           make_output(spec_name, talent_info, talent_str, profileset) + '\n', \
           len(talent_str)


def make_output(spec_name, talent_info, talent_str, output):
    output_str_list = []
    for configuration in talent_str:
        name = get_configuration_name(configuration, spec_name, talent_info)
        output_str_list.append(output.format(name=name, configuration=configuration))
    return '\n'.join(output_str_list)
