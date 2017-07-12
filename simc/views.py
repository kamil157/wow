from django.views.generic import TemplateView


class TalentsView(TemplateView):
    template_name = 'simc/talents.html'

    def get_context_data(self, **kwargs):
        context = super(TalentsView, self).get_context_data(**kwargs)

        import requests
        json = requests.get("https://us.api.battle.net/wow/data/talents?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q").json()

        talents_by_class = []
        for wow_class in json.values():

            talents_by_spec = []
            for spec in wow_class['specs']:

                talent_list = []
                for row_id, row in enumerate(wow_class['talents']):

                    talent_row = []
                    for column, talent in enumerate(row):

                        try:
                            spec_talent = next(t for t in talent if 'spec' in t and t['spec']['name'] == spec['name'])
                        except StopIteration:
                            # If there is no spec info, this talent is for all specs which don't have a talent specified.
                            spec_talent = next(t for t in talent if 'spec' not in t)

                        name = '{}{}'.format(row_id, column)
                        talent_row.append({'id': spec_talent['spell']['id'], 'name': name})

                    talent_list.append(talent_row)

                talents_by_spec.append(talent_list)

            talents_by_class.append(talents_by_spec)

        context['talents'] = talents_by_class
        return context
