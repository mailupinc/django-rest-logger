def test_base_logging_with_standard_request(api_request_factory, middleware_empty_django_response, mocked_logger):
    request = api_request_factory.get("/foo")
    middleware_empty_django_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]


def test_base_logging_with_api_request(api_request_factory, middleware_empty_api_response, mocked_logger):
    request = api_request_factory.get("/foo", format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
