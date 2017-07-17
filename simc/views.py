from itertools import product

import requests
from django.shortcuts import render
from django.views.generic import TemplateView

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
    # TODO view with talents for all specs
    if request.method == 'POST':
        form = TalentsForm(request.POST, **kwargs)
        if form.is_valid():
            choice = form.cleaned_data
            output = get_combinations(choice)
            return render(request, 'simc/talents.html', {'form': form, 'choice': choice, 'output': output})

    else:
        form = TalentsForm(**kwargs)

    return render(request, 'simc/talents.html', {'form': form})


def get_select_spec(request, **kwargs):
    class_json = requests.get(
        'https://eu.api.battle.net/wow/data/character/classes?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q').json()

    spec_json = requests.get(
        'https://eu.api.battle.net/wow/data/talents?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q').json()

    classes = []
    for cls in class_json['classes']:
        wow_class = spec_json[str(cls['id'])]
        classes.append({'class': cls, 'slug': wow_class['class'], 'specs': wow_class['specs']})

    return render(request, 'simc/select_spec.html', {'classes': sorted(classes, key=lambda c: c['slug'])})


class CharacterView(TemplateView):
    template_name = 'simc/character.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterView, self).get_context_data(**kwargs)
        json = requests.get(
            "https://eu.api.battle.net/wow/character/Aggramar/Atuad?fields=talents&locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        context['character'] = json
        return context
