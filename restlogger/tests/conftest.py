from unittest import mock

import pytest
import django
from django.conf import settings
from django.http import HttpResponse
from pytest_django.lazy_django import skip_if_no_django

import restlogger
from restlogger.mixins import ExecutionLogMixin


def pytest_configure():
    settings.configure(
        API_LOGGER_URL_PATH_TO_EXCLUDE=("/path1/",),
        API_LOGGER_KEY_PATH_TO_HASH=(("path", "to", "hash"),),
        API_LOGGER_APP_NAME="Test",
        REST_FRAMEWORK={
            "DEFAULT_RENDERER_CLASSES": [
                "rest_framework.renderers.JSONRenderer",
            ],
            "DEFAULT_PARSER_CLASSES": [
                "rest_framework.parsers.JSONParser",
            ],
        },
        MIDDLEWARE=[
            "restlogger.middleware.RESTRequestLoggingMiddleware",
        ],
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
        GIT_TAG="a-tag",
        GIT_SHA="a-sha",
    )
    django.setup()


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


def get_pdf_api_response(request):
    from rest_framework.renderers import JSONRenderer
    from rest_framework.response import Response

    response = Response(data={"content": "A simple API response"})
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/pdf"
    response.content_type = "application/pdf"
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
def middleware_pdf_api_response():
    skip_if_no_django()

    from restlogger.middleware import RESTRequestLoggingMiddleware

    yield RESTRequestLoggingMiddleware(get_pdf_api_response)


@pytest.fixture()
def api_request_factory():
    """APIRequestFactory instance"""
    skip_if_no_django()

    from rest_framework.test import APIRequestFactory

    yield APIRequestFactory()


@pytest.fixture()
def standard_request_factory():
    """APIRequestFactory instance"""
    skip_if_no_django()

    from django.test import RequestFactory

    yield RequestFactory()


@pytest.fixture
def mocked_logger():
    with mock.patch.object(restlogger.middleware, "log") as mock_logger:
        yield mock_logger


@pytest.fixture
def standard_view_with_mixin():
    from django.views import View

    class TestStandardView(ExecutionLogMixin, View):
        def get(self, request, *args, **kwargs):
            self.start_timing_step("test")
            self.add_log_step("first-step")
            self.add_task_info({"key1": "value"})
            self.add_log_step("second-step", {"step2": "data"})
            self.stop_timing_step("test")
            return HttpResponse("A simple response")

    yield TestStandardView


@pytest.fixture
def api_view_with_mixin():
    from rest_framework.views import APIView

    class TestAPIView(ExecutionLogMixin, APIView):
        def get(self, request, *args, **kwargs):
            self.start_timing_step("test")
            self.add_log_step("first-step")
            self.add_task_info({"key2": "value"})
            self.add_log_step("second-step", {"step2": "data"})
            self.stop_timing_step("test")
            return HttpResponse("A simple response")

    yield TestAPIView


@pytest.fixture
def api_view_with_mixin_no_timing_step_stop():
    from rest_framework.views import APIView

    class TestAPIView(ExecutionLogMixin, APIView):
        def get(self, request, *args, **kwargs):
            self.start_timing_step("test")
            self.start_timing_step("empty")
            self.stop_timing_step("test")
            return HttpResponse("A simple response")

    yield TestAPIView
