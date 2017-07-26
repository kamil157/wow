from datetime import timedelta
from typing import Dict, List, Union

from requests_cache import CachedSession

from wow.settings import WOW_API_SECRET_KEY


class Wowapi:
    def __init__(self, apikey=WOW_API_SECRET_KEY) -> None:
        self.apikey = apikey  # type: str

    def get(self, resource: str, params=None):
        if params is None:
            params = {}
        root = 'https://eu.api.battle.net/wow/'
        params.update({'apikey': self.apikey, 'locale': 'en_US'})

        s = CachedSession(expire_after=timedelta(hours=1))
        return s.get(root + resource, params=params).json()

    def get_classes(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
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
        return self.get('data/character/classes')

    Spell = Dict[str, Union[int, str]]
    Spec = Dict[str, Union[int, str]]
    Talents = List[List[List[Dict[str, Union[Spell, Spec, int]]]]]

    def get_talents(self) -> Dict[str, Dict[str, Union[Talents, str, List[Spec]]]]:
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
                                        'name': str
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
        return self.get('data/talents')
