import json
import logging
from typing import Callable

from .conf import settings

from .utils import apply_hash_filter

log = logging.getLogger("django.request")


class RESTRequestLoggingMiddleware:
    """
    Django Middleware for logging some detailed info of the request/response cycle
    Best suited for using with Django REST Framework (DRF)
    """

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.cached_request_body = None

    def __call__(self, request):
        if settings.API_LOGGER_ENABLED:
            data = self._get_request_info(request)

        response = self.get_response(request)

        if settings.API_LOGGER_ENABLED:
            data.update(self._get_response_info(response))
            apply_hash_filter(data)
            log.info("Execution Log", extra=data)
        return response

    def _get_request_info(self, request) -> dict:
        """
        Extracts info from a request (Django or DRF request object)
        """
        self.cached_request_body = request.body
        jwt_payload = None
        headers = {key: value for key, value in request.headers.items()}
        if auth_headers := headers.get("Authorization"):
            token = self._get_raw_token(auth_headers)
            jwt_payload = self._get_jwt_payload(token)
        try:
            user = request.user
        except AttributeError:
            user = None
        request_data = {
            "request": {
                "path": request.get_full_path(),
                "method": request.method,
                "headers": headers,
                "body": self._get_request_body(),
                "user": user,
                "jwt_payload": jwt_payload,
            }
        }
        return request_data

    @staticmethod
    def _get_raw_token(auth_headers) -> str:
        """
        Extracts the JSON web token from the "Authorization" header
        """
        if parts := auth_headers.split():
            if parts[0] not in ("Bearer", "JWT"):
                return ""
            return parts[1]
        return ""

    @staticmethod
    def _get_jwt_payload(token: str) -> dict:
        """
        Extracts JWT payload from the Authorization headers
        """
        # TODO fake implementation for the moment
        return {"payload": "data"}

    def _get_request_body(self) -> dict:
        """
        Try to get the body of the request, if any
        """
        if not self.cached_request_body:
            return {}
        try:
            body = json.loads(self.cached_request_body)
        except Exception:
            body = None
        return body

    def _get_response_info(self, response) -> dict:
        """
        Extracts info from a response (DRF response object)
        """
        response_data = {
            "response": {
                "data": self._get_response_data(response)
                or "Not a REST Framework response",
                "status_code": response.status_code,
            }
        }
        return response_data

    def _get_response_data(self, response) -> dict:
        """
        Try to get 'data' attribute from response , if any
        """
        try:
            return response.data
        except AttributeError:
            return {}
