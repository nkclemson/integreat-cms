from __future__ import annotations

import json
import logging
from html import unescape
from typing import TYPE_CHECKING
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if TYPE_CHECKING:
    from typing import Any

logger = logging.getLogger(__name__)


class TextlabClient:
    """
    Client for the textlab api.
    Supports login and hix-score retrieval.

    A detailed API documentation can be found at https://comlab-ulm.github.io/swagger-V8/
    """

    def __init__(self, username: str, password: str) -> None:
        if not settings.TEXTLAB_API_ENABLED:
            raise ImproperlyConfigured("Textlab API is disabled")

        self.username = username
        self.password = password
        self.token = None

        self.login()

    def login(self) -> None:
        """
        Authorizes for the textlab api. On success, sets the token attribute.

        :raises urllib.error.HTTPError: If the login was not successful
        """
        data = {"identifier": self.username, "password": self.password}
        response = self.post_request("/user/login", data)
        self.token = response["token"]

    def benchmark(self, text: str) -> float | None:
        """
        Retrieves the hix score of the given text.

        :param text: The text to calculate the score for
        :return: The score, or None if an error occurred
        """
        data = {"text": unescape(text), "locale_name": "de_DE"}
        path = "/benchmark/5"
        response = self.post_request(path, data, self.token)
        return response.get("formulaHix")

    @staticmethod
    def post_request(
        path: str, data: dict[str, str], auth_token: str | None = None
    ) -> dict[str, Any]:
        """
        Sends a request to the api.

        :param path: The api path
        :param data: The data to send
        :param auth_token: The authorization token to use
        :return: The response json dictionary
        :raises urllib.error.HTTPError: If the request failed
        """
        data_json: bytes = json.dumps(data).encode("utf-8")
        request = Request(
            f"{settings.TEXTLAB_API_URL.rstrip('/')}{path}",
            data=data_json,
            method="POST",
        )
        if auth_token:
            request.add_header("authorization", f"Bearer {auth_token}")
        request.add_header("Content-Type", "application/json")
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
