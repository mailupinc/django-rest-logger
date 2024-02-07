import pytest
from rest_framework import status
import django

from restlogger.middleware import RESTRequestLoggingMiddleware


@pytest.mark.freeze_time("2023-01-01", auto_tick_seconds=0.1)
def test_execution_log_mixin_standard(standard_request_factory, standard_view_with_mixin, mocked_logger):
    request = standard_request_factory.get("/foo")
    get_response = standard_view_with_mixin.as_view()
    middleware = RESTRequestLoggingMiddleware(get_response)
    response = middleware(request)

    name, args, kwargs = mocked_logger.mock_calls[0]
    assert response.status_code == status.HTTP_200_OK
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["data"] == "Not a serializable response"
    assert kwargs["extra"]["response"]["status_code"] == status.HTTP_200_OK
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["task_info"]
    assert kwargs["extra"]["task_info"] == {"key1": "value"}
    assert kwargs["extra"]["log_steps"]
    assert len(kwargs["extra"]["log_steps"]) == 2
    assert kwargs["extra"]["log_steps"] == [
        {"msg": "first-step", "detail": {}},
        {"msg": "second-step", "detail": {"step2": "data"}},
    ]
    assert kwargs["extra"]["timing_steps"] == {"test": 0.1}


@pytest.mark.freeze_time("2023-01-01", auto_tick_seconds=0.2)
def test_execution_log_mixin_api(api_request_factory, api_view_with_mixin, mocked_logger):
    request = api_request_factory.get("/foo")
    get_response = api_view_with_mixin.as_view()
    middleware = RESTRequestLoggingMiddleware(get_response)
    response = middleware(request)

    name, args, kwargs = mocked_logger.mock_calls[0]
    assert response.status_code == status.HTTP_200_OK
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["data"] == "Not a serializable response"
    assert kwargs["extra"]["response"]["status_code"] == status.HTTP_200_OK
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["task_info"]
    assert kwargs["extra"]["task_info"] == {"key2": "value"}
    assert kwargs["extra"]["log_steps"]
    assert len(kwargs["extra"]["log_steps"]) == 2
    assert kwargs["extra"]["log_steps"] == [
        {"msg": "first-step", "detail": {}},
        {"msg": "second-step", "detail": {"step2": "data"}},
    ]
    assert kwargs["extra"]["timing_steps"] == {"test": 0.2}


@pytest.mark.freeze_time("2023-01-01", auto_tick_seconds=0.3)
def test_execution_log_mixin_api__timing_step_empty_if_not_stopped(
    api_request_factory, api_view_with_mixin_no_timing_step_stop, mocked_logger
):
    mocked_logger.reset_mock()
    request = api_request_factory.get("/foo")
    get_response = api_view_with_mixin_no_timing_step_stop.as_view()
    middleware = RESTRequestLoggingMiddleware(get_response)
    response = middleware(request)

    name, args, kwargs = mocked_logger.mock_calls[0]
    assert response.status_code == status.HTTP_200_OK
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["timing_steps"] == {"test": 0.6}
