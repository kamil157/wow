import requests
from django.views.generic import TemplateView


class TalentsView(TemplateView):
    template_name = 'simc/talents.html'

    def get_context_data(self, **kwargs):
        context = super(TalentsView, self).get_context_data(**kwargs)

        json = requests.get(
            "https://eu.api.battle.net/wow/data/talents?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        wow_class = json[kwargs['class']]
        # TODO make a class for this json
        spec = wow_class['specs'][int(kwargs['spec'])]['name']
        talents = [
            [self.get_talent_for_spec(spec, talent) for talent in row]
            for row in wow_class['talents']
        ]

        context['talents'] = talents

        return context

    @staticmethod
    def get_talent_for_spec(spec, talent):
        try:
            spec_talent = next(t for t in talent if 'spec' in t and t['spec']['name'] == spec)
        except StopIteration:
            # If there is no spec info, this talent is for all specs which don't have a talent specified.
            spec_talent = next(t for t in talent if 'spec' not in t)
        return spec_talent['spell']


class CharacterView(TemplateView):
    template_name = 'simc/character.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterView, self).get_context_data(**kwargs)
        json = requests.get(
            "https://eu.api.battle.net/wow/character/Aggramar/Atuad?fields=talents&locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        context['character'] = json
        return context
