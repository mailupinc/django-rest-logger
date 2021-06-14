from django.conf import settings


def pytest_configure():
    settings.configure(
        API_LOGGER_URL_PATH_TO_EXCLUDE=("/path1/",),
        API_LOGGER_KEY_PATH_TO_HASH=(("path", "to", "hash"),),
    )
