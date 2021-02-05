from django.conf import settings

settings.API_LOGGER_ENABLED = getattr(settings, "API_LOGGER_ENABLED", True)

settings.API_LOGGER_KEY_PATH_TO_HASH = getattr(
    settings, "API_LOGGER_KEY_PATH_TO_HASH", ()
)
