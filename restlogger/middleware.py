import contextlib
import copy
import json
import logging
from datetime import datetime, timezone
from json import JSONDecodeError
from typing import Callable, Dict

from .conf import settings
from .utils import apply_hash_filter, decode_jwt_token_payload, exclude_path, mask_sensitive_data

log = logging.getLogger("restlogger")


class RESTRequestLoggingMiddleware:
    """
    Django Middleware for logging some detailed info of the request/response cycle
    Best suited for using with Django REST Framework (DRF)
    """

    extra_log_info: Dict[dict, dict] = {}
    view_name: str = ""

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        should_log = settings.API_LOGGER_ENABLED and not exclude_path(request.path)

        if should_log:
            return self.get_respose_and_log_info(request)
        else:
            return self.get_response(request)

    def get_respose_and_log_info(self, request):
        """
        Collect and filter all data to log, get response and return it
        """
        cached_request_body = copy.copy(request.body)
        start_time = datetime.now(timezone.utc)
        response = self.get_response(request)
        finish_time = datetime.now(timezone.utc)
        data = self._get_request_info(request, cached_request_body)
        data.update(self._get_response_info(response))
        data.update(self._get_execution_fields(request, start_time, finish_time))
        data.update(self._get_info_fields())
        apply_hash_filter(data)
        with contextlib.suppress(AttributeError):
            data.update(request.execution_log_info)
        log.info("Execution Log", extra=data)
        return response

    def _get_request_info(self, request, cached_request_body) -> dict:
        """
        Extracts info from a request (Django or DRF request object)
        """
        jwt_payload = None
        headers = dict(request.headers.items())
        if auth_headers := headers.get("Authorization"):
            jwt_payload = self._get_jwt_payload(auth_headers)
        try:
            user = request.user
        except AttributeError:
            user = None
        return {
            "request": {
                "url": request.get_full_path(),
                "method": request.method,
                "headers": headers,
                "body": self._get_request_body(cached_request_body),
                "user": user,
                "jwt_payload": jwt_payload,
            }
        }

    @staticmethod
    def _get_raw_token(auth_headers) -> str:
        """
        Extracts the JSON web token from the "Authorization" header if present
        """
        parts = auth_headers.split()
        return "" if parts[0] not in ("Bearer", "JWT") else parts[1]

    def _get_jwt_payload(self, auth_headers) -> dict:
        """
        Extracts JWT payload from the Authorization headers
        """
        token = self._get_raw_token(auth_headers)
        return decode_jwt_token_payload(token)

    def _get_request_body(self, cached_request_body) -> dict:
        """
        Try to get the body of the request, if any
        """
        if not cached_request_body:
            return {}
        try:
            body = json.loads(cached_request_body)
            mask_sensitive_data(body)
        except JSONDecodeError:
            body = "Not a JSON body"
        except AttributeError:
            body = {}

        return body

    def _get_response_info(self, response) -> dict:
        """
        Extracts info from a response (DRF response object)
        """
        return {
            "response": {
                "data": self._get_response_data(response) or "Not a serializable response",
                "status_code": response.status_code,
            }
        }

    @staticmethod
    def _get_response_data(response) -> dict:
        """
        Try to get response data
        """
        response_content_type = response.headers.get("Content-Type")
        if response_content_type == "application/json":
            try:
                return response.data
            except AttributeError:
                return {}
        if response_content_type == "application/pdf":
            return {"content": "PDF bytes response"}
        try:
            return json.loads(response.content)
        except (UnicodeDecodeError, JSONDecodeError):
            return {}

    @staticmethod
    def _timing_fields(start_time: datetime, end_time: datetime) -> dict:
        """
        Create timing fields, calculating duration based on start and end times
        """
        duration = end_time - start_time
        return {
            "timing": {
                "start": start_time,
                "end": end_time,
                "duration": duration.total_seconds(),
            }
        }

    def _get_execution_fields(self, request, start_time: datetime, finish_time: datetime) -> dict:
        """
        Create execution fields
        """
        try:
            name = request.resolver_match.view_name
        except AttributeError:
            name = ""
        execution = {"app": settings.API_LOGGER_APP_NAME, "name": name}
        execution.update(self._timing_fields(start_time, finish_time))
        return {"execution": execution}

    @staticmethod
    def _get_info_fields() -> dict:
        """
        Create info fields
        """
        info = {"git_sha": getattr(settings, "GIT_SHA", ""), "git_tag": getattr(settings, "GIT_TAG", "")}
        cleaned_info = {key: value for key, value in info.items() if value}
        return {"info": cleaned_info}
