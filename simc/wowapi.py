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
    """
    Returns:
        dict(
            'classes': list(
                dict(
                    'id': int,
                    'mask': int,
                    'name': str,
                    'powerType': str
                )
            )
        )
    """
    return get('character/classes')


def get_talents():
    """
    Returns:
        dict(
            '1': dict(
                'talents': list(
                    list(
                        list(
                            dict(
                                'spell': dict(
                                    'description': str,
                                    'name': str,
                                    'icon': str,
                                    'id': int,
                                    'castTime': str
                                ),
                                'spec': dict(
                                    'role': str,
                                    'description': str,
                                    'icon': str,
                                    'order': int,
                                    'name': str,
                                    'backgroundImage': str
                                ),
                                'tier': int,
                                'column': int
                            )
                        )
                    )
                ),
                'class': str,
                'specs': list(
                    dict(
                        'role': str,
                        'description': str,
                        'icon': str,
                        'order': int,
                        'name': str,
                        'backgroundImage': str
                    )
                )
            )
            '2': ...,
    """
    # TODO would be nice if this structure was defined in code and easier to navigate
    return get('talents')
