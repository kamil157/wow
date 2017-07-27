import os
from functools import lru_cache
from itertools import product
from textwrap import dedent
from typing import List, Tuple, Set

from wow import settings

# In SimulationCraft, 0 means no talent selected
NO_TALENT = '0'


def get_talent_for_spec(spec_name: str, talent):
    try:
        spec_talent = next(t for t in talent if 'spec' in t and t['spec']['name'] == spec_name)
    except StopIteration:
        # If there is no spec info, this talent is for all specs which don't have a talent specified.
        spec_talent = next(t for t in talent if 'spec' not in t)
    return spec_talent['spell']


@lru_cache(maxsize=1)
def get_dictionary() -> Set[str]:
    with open(os.path.join(settings.BASE_DIR, 'simc/dictionary.txt')) as f:
        return set(word.strip() for word in f.readlines())


@lru_cache()
def get_short_talent_name(talent_name: str) -> str:
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


def get_configuration_name(configuration, spec_name: str, talent_info) -> str:
    talent_names = []
    for row, column_choice in enumerate(configuration):
        if column_choice != NO_TALENT:
            talent = talent_info[row][int(column_choice) - 1]
            talent_name = get_talent_for_spec(spec_name, talent)['name']
            talent_names.append(get_short_talent_name(talent_name))
    return ' '.join(talent_names)


def get_configurations(choice, talent_info, spec_name: str) -> Tuple[str, str, int]:  # TODO class/dict for this
    values = [c if c else [NO_TALENT] for c in choice.values()]
    talents = product(*values)
    talent_str = [''.join(talent_choice) for talent_choice in talents]

    copy_output = format_copy_output(spec_name, talent_info, talent_str)
    profileset_output = format_profileset_output(spec_name, talent_info, talent_str)

    return copy_output, profileset_output, len(talent_str)


def format_profileset_output(spec_name: str, talent_info, talent_str: List[str]) -> str:
    # E.g.: profileset."PM Shi MI AF FS LB Kin"=talents=1111111
    output_format = 'profileset."{name}"=talents={configuration}'
    output = make_output(spec_name, talent_info, talent_str, output_format)
    comment = '''
        # Paste this after your simc profile.
        # Profilesets greatly reduce memory usage, 
        # but they might not be fully operational yet.
        
        {output}
        '''
    return dedent(comment).format(output=output)


def format_copy_output(spec_name: str, talent_info, talent_str: List[str]) -> str:
    # E.g.:
    # copy=PM Shi MI AF FS LB Kin
    # talents=1111111
    output_format = ('copy="{name}"\n'
                     'talents={configuration}\n')
    output = make_output(spec_name, talent_info, talent_str, output_format).rstrip()
    comment = '''
        # Paste this after your simc profile.
        # Copy requires memory for each configuration, which might result 
        # in crashing your computer with many configurations.
        
        {output}
        '''
    return dedent(comment).format(output=output)


def make_output(spec_name: str, talent_info, talent_str: List[str], output: str) -> str:
    output_str_list = []
    for configuration in talent_str:
        name = get_configuration_name(configuration, spec_name, talent_info)
        output_str_list.append(output.format(name=name, configuration=configuration))
    return '\n'.join(output_str_list)
