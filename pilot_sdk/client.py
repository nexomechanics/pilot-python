from __future__ import annotations

from dataclasses import dataclass

import httpx

from .exceptions import AuthError, PaymentRequiredError, PilotError, RateLimitError

_BASE_URL = "https://api.pilotnoti.com"


@dataclass
class SendResult:
    remaining: int


class Pilot:
    def __init__(self, api_key: str, base_url: str = _BASE_URL, timeout: float = 10.0):
        self._headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        self._base = base_url.rstrip("/")
        self._timeout = timeout

    def send(self, destination: str, message: str) -> SendResult:
        url = f"{self._base}/v1/forward"
        with httpx.Client(timeout=self._timeout) as client:
            r = client.post(url, headers=self._headers, json={"destination": destination, "message": message})
        return SendResult(remaining=self._handle(r)["remaining"])

    def _handle(self, r: httpx.Response) -> dict:
        if r.status_code == 401:
            raise AuthError(self._err(r, "unauthorized"), r.status_code)
        if r.status_code == 402:
            raise PaymentRequiredError(self._err(r, "payment required"), r.status_code)
        if r.status_code == 403:
            raise PilotError(self._err(r, "forbidden"), r.status_code)
        if r.status_code == 429:
            raise RateLimitError(self._err(r, "rate limit exceeded"), r.status_code)
        if r.status_code >= 400:
            raise PilotError(self._err(r, "request failed"), r.status_code)
        return r.json()

    @staticmethod
    def _err(r: httpx.Response, fallback: str) -> str:
        try:
            return r.json().get("error", fallback)
        except Exception:
            return fallback
