from itertools import product

import requests
from django.shortcuts import render
from django.views.generic import TemplateView

from simc.forms import TalentsForm


def get_combinations(choice):
    result = ''
    sorted_choice = sorted(choice.items())
    # In simcraft, 0 means no talent selected
    values = [c[1] if c[1] else ['0'] for c in sorted_choice]
    talents = product(*values)
    talent_str = [''.join(talent_choice) for talent_choice in talents]

    name = 'Irith'
    output = ('copy="{name}{combination}"\n'
              'talents={combination}\n')

    for combination in talent_str:
        result += output.format(name=name, combination=combination)
        result += '\n'

    return result


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


class CharacterView(TemplateView):
    template_name = 'simc/character.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterView, self).get_context_data(**kwargs)
        json = requests.get(
            "https://eu.api.battle.net/wow/character/Aggramar/Atuad?fields=talents&locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        context['character'] = json
        return context
