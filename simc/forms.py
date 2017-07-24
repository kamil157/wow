from django import forms

from simc.talents import get_talent_for_spec
from simc.widgets import TalentSelectMultiple


class TalentsForm(forms.Form):
    def __init__(self, talent_info, spec_name, *args):
        super().__init__(*args)

        for row_id, row in enumerate(talent_info):
            # Talents in SimulationCraft are numbered from 1
            choices = [(col_id + 1, get_talent_for_spec(spec_name, row[col_id])['name'])
                       for col_id in range(3)]
            talents = [get_talent_for_spec(spec_name, row[col_id]) for col_id in range(3)]
            choice = forms.MultipleChoiceField(choices=choices, label='', required=False,
                                               widget=TalentSelectMultiple(talents=talents, attrs={'class': 'hidden'}))
            self.fields['row_{index}'.format(index=row_id)] = choice
