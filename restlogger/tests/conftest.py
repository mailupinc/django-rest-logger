from unittest import mock

import pytest
from django.conf import settings
from django.http import HttpResponse
from pytest_django.lazy_django import skip_if_no_django

import restlogger


def pytest_configure():
    settings.configure(
        API_LOGGER_URL_PATH_TO_EXCLUDE=("/path1/",),
        API_LOGGER_KEY_PATH_TO_HASH=(("path", "to", "hash"),),
        REST_FRAMEWORK={
            "DEFAULT_RENDERER_CLASSES": [
                "rest_framework.renderers.JSONRenderer",
            ],
            "DEFAULT_PARSER_CLASSES": [
                "rest_framework.parsers.JSONParser",
            ],
        },
    )


def get_simple_django_response(request):
    return HttpResponse("A simple response")


def get_simple_api_response(request):
    from rest_framework.renderers import JSONRenderer
    from rest_framework.response import Response

    response = Response(data={"content": "A simple API response"})
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    return response.render()


@pytest.fixture()
def middleware_empty_django_response():
    skip_if_no_django()

    from restlogger.middleware import RESTRequestLoggingMiddleware

    yield RESTRequestLoggingMiddleware(get_simple_django_response)


@pytest.fixture()
def middleware_empty_api_response():
    skip_if_no_django()

    from restlogger.middleware import RESTRequestLoggingMiddleware

    yield RESTRequestLoggingMiddleware(get_simple_api_response)


@pytest.fixture()
def api_request_factory():
    """APIRequestFactory instance"""
    skip_if_no_django()

    from rest_framework.test import APIRequestFactory

    yield APIRequestFactory()


@pytest.fixture
def mocked_logger():
    with mock.patch.object(restlogger.middleware, "log") as mock_logger:
        yield mock_logger
