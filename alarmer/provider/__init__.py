import abc
from typing import Optional

from alarmer import Alarmer
from alarmer.throttling import Throttling


class Provider(abc.ABC):
    def __init__(self, throttling: Optional[Throttling] = None):
        self.throttling = throttling

    def get_title(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        return (
            f"[{Alarmer.environment}] Exception Alarm: {exc}"
            if exc
            else f"[{Alarmer.environment}] Alarm"
        )

    def send(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        raise NotImplementedError()
