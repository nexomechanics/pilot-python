from __future__ import annotations

from typing import Optional


class PilotError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class AuthError(PilotError):
    pass


class RateLimitError(PilotError):
    pass


class PaymentRequiredError(PilotError):
    pass
