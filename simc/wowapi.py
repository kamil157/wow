from datetime import timedelta
from typing import List, Any, Dict

from django.utils.text import slugify
from requests_cache import CachedSession
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

from wow.settings import WOW_API_CLIENT_ID, WOW_API_CLIENT_SECRET


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
    def __init__(self, client_id=WOW_API_CLIENT_ID, client_secret=WOW_API_CLIENT_SECRET) -> None:
        self.client_id = client_id  # type: str
        self.client_secret = client_secret  # type: str

    def get(self, resource: str, params=None):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://us.battle.net/oauth/token', client_id=self.client_id, client_secret=self.client_secret)

        if params is None:
            params = {}
        root = 'https://us.api.blizzard.com/'
        params.update({'locale': 'en_US', 'namespace': 'static-us', 'access_token': token['access_token']})

        session = CachedSession(expire_after=timedelta(hours=1))
        return session.get(root + resource, params=params).json()

    def get_classes(self) -> List[WowClass]:  # TODO get rid of this?
        data = self.get('data/wow/playable-class/index')
        return [WowClass(c) for c in data['classes']]

    def get_talents(self) -> Talents:
        classes = self.get_classes()
        return Talents(self.get('wow/data/talents'), classes)
