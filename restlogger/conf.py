import logging

from django.conf import settings

settings.API_LOGGER_ENABLED = getattr(settings, "API_LOGGER_ENABLED", True)

settings.API_LOGGER_URL_PATH_TO_EXCLUDE = getattr(
    settings, "API_LOGGER_URL_PATH_TO_EXCLUDE", ()
)

settings.API_LOGGER_KEY_PATH_TO_HASH = getattr(
    settings, "API_LOGGER_KEY_PATH_TO_HASH", ()
)
settings.API_LOGGER_KEY_PATH_TO_HASH += (("request", "body", "password"),)

settings.API_LOGGER_DEFAULT_LOG_LEVEL = getattr(
    settings, "API_LOGGER_DEFAULT_LOG_LEVEL", logging.INFO
)
