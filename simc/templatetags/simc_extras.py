from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def icon(value):
    """Changes icon names from blizzard version to wowhead."""
    icons = {
        'spell_frost_ringoffrost': 'spell_frost_ring-of-frost',
        'spell_priest_voidflay': 'spell_priest_void-flay',
        'spell_frost_iceshards': 'spell_frost_ice-shards',
        'trade_archaeology_zinrokhsword': 'trade_archaeology_zinrokh-sword',
    }
    if value in icons:
        return icons[value]
    return value
