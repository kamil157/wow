import requests
from django import forms

from simc.widgets import TalentSelectMultiple


class TalentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # TODO allow selecting class / spec in a view
        kw_class = kwargs.pop('class_id')
        kw_spec = kwargs.pop('spec')
        super().__init__(*args, **kwargs)

        # TODO make a class for this json
        json = requests.get(
            "https://eu.api.battle.net/wow/data/talents?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        wow_class = json[kw_class]
        spec_name = wow_class['specs'][int(kw_spec)]['name']

        for row_id, row in enumerate(wow_class['talents']):
            # Talents in simcraft are numbered from 1
            choices = [(col_id + 1, self.get_talent_for_spec(spec_name, row[col_id])['name'])
                       for col_id in range(3)]
            talents = [self.get_talent_for_spec(spec_name, row[col_id]) for col_id in range(3)]
            choice = forms.MultipleChoiceField(choices=choices, label='', required=False,
                                               widget=TalentSelectMultiple(talents=talents, attrs={'class': 'hidden'}))
            self.fields['row_{index}'.format(index=row_id)] = choice

    @staticmethod
    def get_talent_for_spec(spec, talent):
        try:
            spec_talent = next(t for t in talent if 'spec' in t and t['spec']['name'] == spec)
        except StopIteration:
            # If there is no spec info, this talent is for all specs which don't have a talent specified.
            spec_talent = next(t for t in talent if 'spec' not in t)
        return spec_talent['spell']
