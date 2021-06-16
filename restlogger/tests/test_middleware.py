def test_base_logging_with_standard_request(
    API_request_factory, middleware_empty_django_response, mocked_logger
):
    request = API_request_factory.get("/foo")
    middleware_empty_django_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["path"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200


def test_base_logging_with_api_request(
    API_request_factory, middleware_empty_api_response, mocked_logger
):
    request = API_request_factory.get("/foo", format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["path"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
