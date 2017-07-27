import logging
from collections import OrderedDict

from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render

from simc.forms import TalentsForm
from simc.talents import get_configurations
from simc.wowapi import Wowapi

logger = logging.getLogger('simc')


def get_talents(request: HttpRequest, class_slug: str, spec_slug: str) -> HttpResponse:
    wowapi = Wowapi()

    # Get class from slug
    talents_info = wowapi.get_talents()
    try:
        wow_class = next(c for c in talents_info.talents if c.slug == class_slug)
    except StopIteration:
        raise Http404('Invalid class slug.')

    # Get spec from slug
    try:
        spec = next(s for s in wow_class.specs if s.slug == spec_slug)
        spec_name = spec.name
    except StopIteration:
        raise Http404('Invalid spec slug.')

    # Prepare form
    view_data = {'output': None, 'class_name': wow_class.name, 'spec': spec}
    if request.method == 'POST':
        form = TalentsForm(wow_class.talents, spec_name, request.POST)
        if form.is_valid():
            # Log talent choice
            sorted_choices = OrderedDict(sorted(form.cleaned_data.items()))
            sorted_choices_str = [''.join(c) for c in sorted_choices.values()]
            logger.info("{} {} {}".format(wow_class.name, spec_name, sorted_choices_str))

            # Get talent configurations
            copy, profileset, num_configs = get_configurations(sorted_choices, wow_class.talents, spec_name)
            view_data['copy'] = copy
            view_data['profileset'] = profileset
            view_data['num_configs'] = num_configs

    else:
        form = TalentsForm(wow_class.talents, spec_name)

    view_data['form'] = form
    return render(request, 'simc/talents.html', view_data)


def get_select_spec(request: HttpRequest) -> HttpResponse:
    wowapi = Wowapi()
    talents = wowapi.get_talents()
    return render(request, 'simc/select_spec.html', {'classes': sorted(talents.talents, key=lambda c: c.slug)})
