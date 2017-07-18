from datetime import timedelta

from requests_cache import CachedSession

from wow import settings


def get(resource):
    root = 'https://eu.api.battle.net/wow/data/'
    if settings.WOW_API_SECRET_KEY is None:
        raise Exception('WOW_API_SECRET_KEY is not set.')
    params = {'apikey': settings.WOW_API_SECRET_KEY, 'locale': 'en_US'}

    s = CachedSession(expire_after=timedelta(hours=1))
    return s.get(root + resource, params=params).json()


def get_classes():
    return get('character/classes')


def get_talents():
    # TODO would be nice if this structure was defined in code and easier to navigate
    return get('talents')
