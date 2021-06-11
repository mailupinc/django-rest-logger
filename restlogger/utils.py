import hashlib

from django.conf import settings


def apply_hash_filter(data: dict) -> dict:
    """
    Iterates over the filter tuples from settings and call hashing function on them
    """
    for key_path in settings.API_LOGGER_KEY_PATH_TO_HASH:
        find_and_hash_key(data, key_path)
    return data


def hash_object(object) -> str:
    return "Hash " + hashlib.md5(str(object).encode("utf-8")).hexdigest()


def find_and_hash_key(data: dict, key_path: tuple):
    """
    Given a dict and a path to a key (as a tuple), calls the hashing utility on it
    """
    try:
        for key in key_path[:-1]:
            data = data[key]
        if data[key_path[-1]]:
            data[key_path[-1]] = hash_object(data[key_path[-1]])
    except (KeyError, TypeError):
        pass


def exclude_path(path: str) -> bool:
    for excluded_path in settings.API_LOGGER_URL_PATH_TO_EXCLUDE:
        if path.startswith(excluded_path):
            return True
    return False
