import contextlib
import hashlib
from typing import Union

import jwt
from django.conf import settings
from jwt.exceptions import DecodeError


def apply_hash_filter(data: dict) -> dict:
    """
    Iterates over the filter tuples from settings and call hashing function on them
    """
    for key_path in settings.API_LOGGER_KEY_PATH_TO_HASH:
        find_and_hash_key(data, key_path)
    return data


def mask_sensitive_data(data: Union[dict, list]) -> Union[dict, list]:
    """
    Iterates over data dict and mask any key that contains one of sensitive keys defined in settings
    """
    if isinstance(data, dict):
        return mask_sensitive_data_dict(data)
    if isinstance(data, list):
        for item in data:
            mask_sensitive_data(item)
        return data
    return data


def mask_sensitive_data_dict(data: dict) -> dict:
    for key, value in data.items():
        if any(sensitive_key in key for sensitive_key in settings.API_LOGGER_SENSITIVE_KEYS):
            if isinstance(value, list):
                data[key] = ["***FILTERED***" for item in data[key]]
            else:
                data[key] = "***FILTERED***"
        if isinstance(value, dict):
            mask_sensitive_data(value)
    return data


def hash_object(object) -> str:
    return "Hash " + hashlib.md5(str(object).encode("utf-8")).hexdigest()


def find_and_hash_key(data: dict, key_path: tuple):
    """
    Given a dict and a path to a key (as a tuple), calls the hashing utility on it
    """
    with contextlib.suppress(KeyError, TypeError):
        for key in key_path[:-1]:
            data = data[key]
        if data[key_path[-1]]:
            data[key_path[-1]] = hash_object(data[key_path[-1]])


def exclude_path(path: str) -> bool:
    """
    Check if given path is in a list defined on Settings
    """
    return any(path.startswith(excluded_path) for excluded_path in settings.API_LOGGER_URL_PATH_TO_EXCLUDE)


def decode_jwt_token_payload(token: str) -> dict:
    """
    Extracts payload from a JWT token
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except DecodeError:
        payload = {}
    return payload
