import logging

from django.conf import settings

settings.API_LOGGER_ENABLED = getattr(settings, "API_LOGGER_ENABLED", True)

settings.API_LOGGER_URL_PATH_TO_EXCLUDE = getattr(settings, "API_LOGGER_URL_PATH_TO_EXCLUDE", ())

settings.API_LOGGER_HASH_RESPONSE_DATA = getattr(settings, "API_LOGGER_HASH_RESPONSE_DATA", True)

settings.API_LOGGER_KEY_PATH_TO_HASH = getattr(settings, "API_LOGGER_KEY_PATH_TO_HASH", ())

if settings.API_LOGGER_HASH_RESPONSE_DATA:
    settings.API_LOGGER_KEY_PATH_TO_HASH += (("response", "data"),)

settings.API_LOGGER_SENSITIVE_KEYS = getattr(settings, "API_LOGGER_SENSITIVE_KEYS", ())

settings.API_LOGGER_SENSITIVE_KEYS += ("password",)

settings.API_LOGGER_DEFAULT_LOG_LEVEL = getattr(settings, "API_LOGGER_DEFAULT_LOG_LEVEL", logging.INFO)

settings.API_LOGGER_APP_NAME = getattr(settings, "API_LOGGER_APP_NAME", "")
