from itertools import product

import requests
from django.shortcuts import render
from django.views.generic import TemplateView

from simc import wowapi
from simc.forms import TalentsForm


def get_combinations(choice):
    sorted_choice = sorted(choice.items())
    # In simcraft, 0 means no talent selected
    values = [c[1] if c[1] else ['0'] for c in sorted_choice]
    talents = product(*values)
    talent_str = [''.join(talent_choice) for talent_choice in talents]

    output = ('copy="{combination}"\n'
              'talents={combination}\n')

    return '\n'.join(output.format(combination=combination) for combination in talent_str)


def get_talents(request, **kwargs):
    if request.method == 'POST':
        form = TalentsForm(request.POST, **kwargs)
        if form.is_valid():
            choice = form.cleaned_data
            output = get_combinations(choice)
            return render(request, 'simc/talents.html', {'form': form, 'choice': choice, 'output': output})

    else:
        form = TalentsForm(**kwargs)

    return render(request, 'simc/talents.html', {'form': form})


def get_select_spec(request):
    all_class_info = wowapi.get_classes()
    spec_json = wowapi.get_talents()

    classes = []
    for class_info in all_class_info['classes']:
        wow_class = spec_json[str(class_info['id'])]
        icon = 'classicon_{}'.format(wow_class['class'].replace('-', ''))
        classes.append({'class_info': class_info, 'specs': wow_class['specs'], 'slug': wow_class['class'], 'icon': icon})

    return render(request, 'simc/select_spec.html', {'classes': sorted(classes, key=lambda c: c['slug'])})


class CharacterView(TemplateView):
    template_name = 'simc/character.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterView, self).get_context_data(**kwargs)
        json = requests.get(
            "https://eu.api.battle.net/wow/character/Aggramar/Atuad?fields=talents&locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        context['character'] = json
        return context
