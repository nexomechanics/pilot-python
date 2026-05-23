from __future__ import annotations

from dataclasses import dataclass

import httpx

_BASE_URL = "https://tools.nexomechanics.com/api/pilot"


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
        r.raise_for_status()
        return SendResult(remaining=r.json()["remaining"])
