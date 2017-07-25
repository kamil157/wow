import logging
from collections import OrderedDict

from django.core.mail import mail_admins
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify

from simc import wowapi
from simc.forms import TalentsForm
from simc.talents import get_configurations

logger = logging.getLogger('simc')


def get_talents(request, class_slug, spec_slug):
    # Get class name from slug
    class_info = wowapi.get_classes()['classes']
    try:
        class_name = next(c['name'] for c in class_info if slugify(c['name']) == class_slug)
    except StopIteration:
        raise Http404('Invalid class slug.')

    # Get spec from slug
    talents_info = wowapi.get_talents()
    wow_class = next(c for c in talents_info.values() if c['class'] == class_slug)
    try:
        spec = next(s for s in wow_class['specs'] if slugify(s['name']) == spec_slug)
        spec_name = spec['name']
    except StopIteration:
        raise Http404('Invalid spec slug.')

    # Prepare form
    view_data = {'output': None, 'class_name': class_name, 'spec': spec}
    if request.method == 'POST':
        form = TalentsForm(wow_class['talents'], spec_name, request.POST)
        if form.is_valid():
            # Log talent choice
            sorted_choices = OrderedDict(sorted(form.cleaned_data.items()))
            sorted_choices_str = [''.join(c) for c in sorted_choices.values()]
            logger.info("{} {} {}".format(class_name, spec_name, sorted_choices_str))

            # Get talent configurations
            copy, profileset, num_configs = get_configurations(sorted_choices, wow_class['talents'], spec_name)
            view_data['copy'] = copy
            view_data['profileset'] = profileset
            view_data['num_configs'] = num_configs

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
