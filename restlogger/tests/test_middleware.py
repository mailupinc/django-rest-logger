from unittest import mock

from django.http import HttpResponse, HttpResponseServerError
from django.test import RequestFactory, SimpleTestCase

import restlogger
from restlogger.middleware import RESTRequestLoggingMiddleware


def get_empty_response(request):
    return HttpResponse()


def get_response_server_error(request):
    return HttpResponseServerError()


class RESTRequestLoggingMiddlewareTest(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RESTRequestLoggingMiddleware(get_empty_response)

    @mock.patch.object(restlogger.middleware, "log")
    def test_base_logging(self, mock_logger):
        request = self.factory.get("/foo")
        self.middleware(request)
        name, args, kwargs = mock_logger.mock_calls[0]
        assert name == "info"
        assert kwargs["extra"]
        assert kwargs["extra"]["request"]["path"] == "/foo"
        assert kwargs["extra"]["request"]["method"] == "GET"
        assert kwargs["extra"]["response"]
        assert kwargs["extra"]["response"]["status_code"] == 200
