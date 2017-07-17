import requests_cache


def get_classes():
    s = requests_cache.CachedSession()
    return s.get(
        'https://eu.api.battle.net/wow/data/character/classes?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q').json()


def get_talents():
    # TODO make a class for this json
    s = requests_cache.CachedSession()
    return s.get(
        'https://eu.api.battle.net/wow/data/talents?locale=en_US&apikey=4uhe36pa65u5nvacajwpkz4s9jzjzd8q').json()
