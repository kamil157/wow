from django import forms
from django.utils.text import slugify

from simc import wowapi
from simc.widgets import TalentSelectMultiple


class TalentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kw_class = kwargs.pop('class_slug')
        kw_spec = kwargs.pop('spec')
        super().__init__(*args, **kwargs)

        talents_info = wowapi.get_talents()
        wow_class = next(c for c in talents_info.values() if c['class'] == kw_class)
        spec_name = next(s for s in wow_class['specs'] if slugify(s['name']) == kw_spec)['name']

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
