from django.test import override_settings


VALID_JWT = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjM0LCJpYXQiOjE1MTYyMzkwMjJ9"
    ".tsvf23UrZ9144-QZZRVundGdr2jXEppJ0fbpLFhIQJc"
)

INVALID_JWT = (
    "XXXXXGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNCIsImlhdCI6MTUxNjIzOTAyMn0"
    ".XiCMgux66NUGCgHHS3TwodfZ9sRlQDnQSOIR9YLSa6A"
)


def test_base_logging_with_standard_get_request(
    standard_request_factory, middleware_empty_django_response, mocked_logger
):
    request = standard_request_factory.get("/foo")
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
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_api_get_request(api_request_factory, middleware_empty_api_response, mocked_logger):
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
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_api_get_request_pdf_response(
    api_request_factory, middleware_pdf_api_response, mocked_logger
):
    request = api_request_factory.get("/foo", format="json")
    middleware_pdf_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == {"content": "PDF bytes response"}
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]


@override_settings(API_LOGGER_KEY_PATH_TO_HASH=(("response", "data"),))
def test_base_logging_with_api_get_request_pdf_response__hashed(
    api_request_factory, middleware_pdf_api_response, mocked_logger
):
    request = api_request_factory.get("/foo", format="json")
    middleware_pdf_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "GET"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == "Hash 57f786d902068a37fb08cefcd9e57e5e"
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]


def test_base_logging_with_api_post_request(api_request_factory, middleware_empty_api_response, mocked_logger):
    request = api_request_factory.post("/foo", {"key": "value"}, format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo"
    assert kwargs["extra"]["request"]["method"] == "POST"
    assert kwargs["extra"]["request"]["body"] == {"key": "value"}
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == {"content": "A simple API response"}
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_standard_post_request(
    standard_request_factory, middleware_empty_django_response, mocked_logger
):
    request = standard_request_factory.post("/foo/", {"key": "value"})
    middleware_empty_django_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo/"
    assert kwargs["extra"]["request"]["method"] == "POST"
    assert kwargs["extra"]["request"]["body"] == "Not a JSON body"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == "Not a serializable response"
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_api_patch_request(api_request_factory, middleware_empty_api_response, mocked_logger):
    request = api_request_factory.patch("/foo/", {"key": "value"}, format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo/"
    assert kwargs["extra"]["request"]["method"] == "PATCH"
    assert kwargs["extra"]["request"]["body"] == {"key": "value"}
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == {"content": "A simple API response"}
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_standard_patch_request(
    standard_request_factory, middleware_empty_django_response, mocked_logger
):
    request = standard_request_factory.patch("/foo/", {"key": "value"})
    middleware_empty_django_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo/"
    assert kwargs["extra"]["request"]["method"] == "PATCH"
    assert kwargs["extra"]["request"]["body"] == "Not a JSON body"
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == "Not a serializable response"
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_api_delete_request(api_request_factory, middleware_empty_api_response, mocked_logger):
    request = api_request_factory.delete("/foo/", format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo/"
    assert kwargs["extra"]["request"]["method"] == "DELETE"
    assert kwargs["extra"]["request"]["body"] == {}
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == {"content": "A simple API response"}
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_standard_delete_request(
    standard_request_factory, middleware_empty_django_response, mocked_logger
):
    request = standard_request_factory.delete("/foo/")
    middleware_empty_django_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["url"] == "/foo/"
    assert kwargs["extra"]["request"]["method"] == "DELETE"
    assert kwargs["extra"]["request"]["body"] == {}
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]
    assert kwargs["extra"]["response"]["status_code"] == 200
    assert kwargs["extra"]["response"]["data"] == "Not a serializable response"
    assert kwargs["extra"]["execution"]
    assert kwargs["extra"]["execution"]["name"] == ""
    assert kwargs["extra"]["execution"]["app"] == "Test"
    assert kwargs["extra"]["execution"]["timing"]
    assert kwargs["extra"]["execution"]["timing"]["start"]
    assert kwargs["extra"]["execution"]["timing"]["end"]
    assert kwargs["extra"]["execution"]["timing"]["duration"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_base_logging_with_api_request_jwt_ok(api_request_factory, middleware_empty_api_response, mocked_logger):
    request = api_request_factory.get("/foo", format="json", HTTP_AUTHORIZATION=f"Bearer {VALID_JWT}")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["jwt_payload"] == {"user_id": 1234, "iat": 1516239022}


def test_base_logging_with_api_request_invalid_jwt(api_request_factory, middleware_empty_api_response, mocked_logger):
    request = api_request_factory.get("/foo", format="json", HTTP_AUTHORIZATION=f"Bearer {INVALID_JWT}")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["jwt_payload"] == {}


def test_base_logging_with_api_request_basic_auth_headers_ok(
    api_request_factory, middleware_empty_api_response, mocked_logger
):
    request = api_request_factory.get("/foo", format="json", HTTP_AUTHORIZATION="Basic YWxhZGRpbjpvcGVuc2VzYW1l")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["jwt_payload"] == {}


def test_base_logging_with_api_request_other_auth_headers_ok(
    api_request_factory, middleware_empty_api_response, mocked_logger
):
    request = api_request_factory.get("/foo", format="json", HTTP_AUTHORIZATION="an-api-key")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert kwargs["extra"]
    assert kwargs["extra"]["request"]["jwt_payload"] == {}


def test_skip_log_if_path_is_excluded(standard_request_factory, middleware_empty_api_response, mocked_logger):
    request = standard_request_factory.get("/path1/", format="json")
    middleware_empty_api_response(request)
    mocked_logger.assert_not_called()


def test_logging_with_api_post__mask_sensitive_data(api_request_factory, middleware_empty_api_response, mocked_logger):
    payload = {
        "user": "myuser",
        "password": "mypassword",
        "nested_1": {
            "user": "myuser",
            "password_old": "mypassword",
            "nested_2": {"user": "myuser", "new_password": "mypassword"},
        },
        "passwords_list": ["mypassword", "mypassword2", "mypassword3"],
    }
    request = api_request_factory.patch("/foo/", data=payload, format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    request_body = kwargs["extra"]["request"]["body"]
    assert request_body["password"] == "***FILTERED***"
    assert request_body["nested_1"]["password_old"] == "***FILTERED***"
    assert request_body["nested_1"]["nested_2"]["new_password"] == "***FILTERED***"
    assert request_body["passwords_list"] == ["***FILTERED***", "***FILTERED***", "***FILTERED***"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha", "git_tag": "a-tag"}


def test_logging_with_api_post__mask_sensitive_data_ok_if_list(
    api_request_factory, middleware_empty_api_response, mocked_logger
):
    payload = [
        {"user": "myuser1", "password": "mypassword1"},
        "astring",
        {"nested_1": {"user": "myuser", "password_old": "mypassword"}},
        42,
    ]
    request = api_request_factory.patch("/foo/", data=payload, format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    request_body = kwargs["extra"]["request"]["body"]
    assert request_body == [
        {"user": "myuser1", "password": "***FILTERED***"},
        "astring",
        {"nested_1": {"user": "myuser", "password_old": "***FILTERED***"}},
        42,
    ]


def test_logging_with_api_get__no_git_sha_tag(
    settings, api_request_factory, middleware_empty_api_response, mocked_logger
):
    delattr(settings, "GIT_SHA")
    delattr(settings, "GIT_TAG")
    request = api_request_factory.get("/foo", format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["info"] == {}


def test_logging_with_api_get__only_git_sha(
    settings, api_request_factory, middleware_empty_api_response, mocked_logger
):
    delattr(settings, "GIT_TAG")
    request = api_request_factory.get("/foo", format="json")
    middleware_empty_api_response(request)
    name, args, kwargs = mocked_logger.mock_calls[0]
    assert name == "info"
    assert kwargs["extra"]
    assert kwargs["extra"]["info"] == {"git_sha": "a-sha"}
