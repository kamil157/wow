import os
from collections import OrderedDict
from itertools import product

import logging

from functools import lru_cache
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify

from simc import wowapi
from simc.forms import TalentsForm
from simc.talents import get_talent_for_spec
from wow import settings

logger = logging.getLogger('simc')


def get_configurations(choice, talent_info, spec_name):
    # TODO annotate types
    # In simcraft, 0 means no talent selected
    values = [c if c else ['0'] for c in choice.values()]
    talents = product(*values)
    talent_str = [''.join(talent_choice) for talent_choice in talents]

    output = ('copy="{name}"\n'
              'talents={configuration}\n')

    output_str_list = []
    for configuration in talent_str:
        name = get_configuration_name(configuration, spec_name, talent_info)
        output_str_list.append(output.format(name=name, configuration=configuration))

    return '\n'.join(output_str_list), len(talent_str)


def get_configuration_name(configuration, spec_name, talent_info):
    talent_names = []
    for row, column_choice in enumerate(configuration):
        # In simcraft, 0 means no talent selected
        if column_choice != '0':
            talent = talent_info[row][int(column_choice) - 1]
            talent_name = get_talent_for_spec(spec_name, talent)['name']
            talent_names.append(get_short_talent_name(talent_name))
    return ' '.join(talent_names)


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


def get_talents(request, **kwargs):
    kw_class = kwargs.pop('class_slug')
    kw_spec = kwargs.pop('spec')

    class_info = wowapi.get_classes()['classes']
    try:
        class_name = next(c['name'] for c in class_info if slugify(c['name']) == kw_class)
    except StopIteration:
        raise Http404('Invalid class slug.')

    talents_info = wowapi.get_talents()
    wow_class = next(c for c in talents_info.values() if c['class'] == kw_class)
    try:
        spec = next(s for s in wow_class['specs'] if slugify(s['name']) == kw_spec)
        spec_name = spec['name']
    except StopIteration:
        raise Http404('Invalid spec slug.')

    view_data = {'output': None, 'class_name': class_name, 'spec': spec}
    if request.method == 'POST':
        form = TalentsForm(wow_class['talents'], spec_name, request.POST)
        if form.is_valid():
            sorted_choices = OrderedDict(sorted(form.cleaned_data.items()))
            sorted_choices_str = [''.join(c) for c in sorted_choices.values()]
            logger.info("{} {} {}".format(class_name, spec_name, sorted_choices_str))
            output, num_configs = get_configurations(sorted_choices, wow_class['talents'], spec_name)
            view_data.update({'output': output, 'num_configs': num_configs})

    else:
        form = TalentsForm(wow_class['talents'], spec_name)

    view_data['form'] = form
    return render(request, 'simc/talents.html', view_data)


def get_select_spec(request):
    all_class_info = wowapi.get_classes()
    spec_json = wowapi.get_talents()

    classes = []
    for class_info in all_class_info['classes']:
        wow_class = spec_json[str(class_info['id'])]
        icon = 'classicon_{}'.format(wow_class['class'].replace('-', ''))
        classes.append(
            {'class_info': class_info, 'specs': wow_class['specs'], 'slug': wow_class['class'], 'icon': icon})

    return render(request, 'simc/select_spec.html', {'classes': sorted(classes, key=lambda c: c['slug'])})
