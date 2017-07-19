from itertools import product

from django.shortcuts import render
from django.utils.text import slugify

from simc import wowapi
from simc.forms import TalentsForm
from simc.talents import get_talent_for_spec


def get_configurations(choice, talent_info, spec_name):
    # TODO annotate types
    sorted_choice = sorted(choice.items())
    # In simcraft, 0 means no talent selected
    values = [c[1] if c[1] else ['0'] for c in sorted_choice]
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

            words = talent_name.split()
            if len(words) == 1:
                talent_names.append(talent_name[:3])
            else:
                talent_names.append(''.join(w[0] for w in words))
    return ' '.join(talent_names)


def get_talents(request, **kwargs):
    kw_class = kwargs.pop('class_slug')
    kw_spec = kwargs.pop('spec')

    class_info = wowapi.get_classes()['classes']
    class_name = next(c['name'] for c in class_info if slugify(c['name']) == kw_class)

    talents_info = wowapi.get_talents()
    wow_class = next(c for c in talents_info.values() if c['class'] == kw_class)
    spec = next(s for s in wow_class['specs'] if slugify(s['name']) == kw_spec)

    view_data = {}
    if request.method == 'POST':
        form = TalentsForm(wow_class['talents'], spec['name'], request.POST)
        if form.is_valid():
            output, num_configs = get_configurations(form.cleaned_data, wow_class['talents'], spec['name'])
            view_data.update({'output': output, 'num_configs': num_configs})

    else:
        form = TalentsForm(wow_class['talents'], spec['name'])

    view_data.update({'form': form, 'class': class_name, 'spec': spec})
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
