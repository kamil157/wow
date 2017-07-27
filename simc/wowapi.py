from datetime import timedelta
from typing import List, Any, Dict

from django.utils.text import slugify
from requests_cache import CachedSession

from wow.settings import WOW_API_SECRET_KEY


class WowClass:
    def __init__(self, data) -> None:
        self.id = data['id']  # type: int
        self.name = data['name']  # type: str
        self.slug = slugify(self.name)  # type: str

    # TODO add better str/repr to classes in this module
    def __repr__(self):
        return "{} {}".format(self.id, self.name)


class ClassTalents:
    def __init__(self, class_id, value, name) -> None:
        self.id = class_id  # type: int
        self.name = name  # type: str
        self.slug = value['class']  # type: str
        self.icon = 'classicon_{}'.format(self.slug.replace('-', ''))  # type: str
        self.talents = [[column for column in row] for row in value['talents']]  # type: List[List[Dict[str, Any]]]
        self.specs = [Spec(data) for data in value['specs']]  # type: List[Spec]

    def __repr__(self):
        return "{} {}".format(self.id, self.slug)


class Spec:
    def __init__(self, data) -> None:
        self.name = data['name']  # type: str
        self.slug = slugify(self.name)  # type: str
        self.icon = data['icon']  # type: str


class Talent:
    def __init__(self, data) -> None:
        # TODO real fields instead of data
        self.data = data


class Talents: # TODO just use a List[ClassTalents]
    def __init__(self, data, classes) -> None:
        data = {int(k): v for k, v in data.items()}
        getName = lambda k: next(c.name for c in classes if c.id == k)
        self.talents = [ClassTalents(k, v, getName(k)) for k, v in sorted(data.items())]

    def __repr__(self):
        return self.talents.__repr__()


class Wowapi:
    def __init__(self, apikey=WOW_API_SECRET_KEY) -> None:
        self.apikey = apikey  # type: str

    def get(self, resource: str, params=None):
        if params is None:
            params = {}
        root = 'https://eu.api.battle.net/wow/'
        params.update({'apikey': self.apikey, 'locale': 'en_US'})

        session = CachedSession(expire_after=timedelta(hours=1))
        return session.get(root + resource, params=params).json()

    def get_classes(self) -> List[WowClass]:  # TODO get rid of this?
        data = self.get('data/character/classes')
        return [WowClass(c) for c in data['classes']]

    def get_talents(self) -> Talents:
        classes = self.get_classes()
        return Talents(self.get('data/talents'), classes)
