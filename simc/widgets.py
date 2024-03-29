from django.forms import CheckboxSelectMultiple


class TalentSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, talents, *args, **kwargs) -> None:
        self.talents = talents
        super().__init__(*args, **kwargs)

    template_name = 'simc/widgets/talents.html'

    def optgroups(self, name, value, attrs=None):
        groups = super().optgroups(name, value, attrs)
        groups = [(n, v, a, self.talents[i]) for i, (n, v, a) in enumerate(groups)]
        return groups
