import contextlib
import json
import logging
from datetime import datetime, timezone
from json import JSONDecodeError
from typing import Callable, Dict

from .conf import settings
from .utils import apply_hash_filter, decode_jwt_token_payload, exclude_path

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
        self.cached_request_body = None
        self.request_content_type = None

    def __call__(self, request):
        should_log = settings.API_LOGGER_ENABLED and not exclude_path(request.path)

        if should_log:
            return self.get_respose_and_log_info(request)
        else:
            return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        with contextlib.suppress(AttributeError):
            self.extra_log_info["task_info"] = getattr(view_func.view_class, "task_info", {})
            self.extra_log_info["log_steps"] = getattr(view_func.view_class, "task_info", {})
            self.extra_log_info["timing_steps"] = getattr(view_func.view_class, "task_info", {})
        return None

    def get_respose_and_log_info(self, request):
        """
        Collect and filter all data to log, get response and return it
        """
        data = self._get_request_info(request)
        start_time = datetime.now(timezone.utc)
        response = self.get_response(request)
        finish_time = datetime.now(timezone.utc)
        data.update(self._get_response_info(response))
        apply_hash_filter(data)
        data.update(self.execution_fields(request, start_time, finish_time))
        data.update(self.extra_log_info)
        log.info("Execution Log", extra=data)
        return response

    def _get_request_info(self, request) -> dict:
        """
        Extracts info from a request (Django or DRF request object)
        """
        self.cached_request_body = request.body
        jwt_payload = None
        headers = dict(request.headers.items())
        self.request_content_type = headers.get("Content-Type")
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
                "body": self._get_request_body(),
                "user": user,
                "jwt_payload": jwt_payload,
            }
        }

    @staticmethod
    def _get_raw_token(auth_headers) -> str:
        """
        Extracts the JSON web token from the "Authorization" header if present
        """
        if parts := auth_headers.split():
            return "" if parts[0] not in ("Bearer", "JWT") else parts[1]
        return ""

    def _get_jwt_payload(self, auth_headers) -> dict:
        """
        Extracts JWT payload from the Authorization headers
        """
        token = self._get_raw_token(auth_headers)
        return decode_jwt_token_payload(token)

    def _get_request_body(self) -> dict:
        """
        Try to get the body of the request, if any
        """
        if not self.cached_request_body:
            return {}
        try:
            if self.request_content_type == "application/json":
                body = json.loads(self.cached_request_body)
            else:
                body = {"content": self.cached_request_body.decode()}
        except (AttributeError, JSONDecodeError):
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
    def timing_fields(start_time: datetime, finish_time: datetime) -> dict:
        """
        Create timing fields, calculating duration based on start and finish times
        """
        duration = finish_time - start_time
        return {
            "timing": {
                "start": start_time,
                "end": finish_time,
                "duration": duration.total_seconds(),
            }
        }

    def execution_fields(self, request, start_time: datetime, finish_time: datetime) -> dict:
        """
        Create execution field
        """
        try:
            name = request.resolver_match.view_name
        except AttributeError:
            name = ""
        execution = {"app": settings.API_LOGGER_APP_NAME, "name": name}
        execution.update(self.timing_fields(start_time, finish_time))
        return {"execution": execution}
