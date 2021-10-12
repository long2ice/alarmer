import abc
from typing import Optional

from alarmer.throttling import Throttling


class Provider(abc.ABC):
    def __init__(self, throttling: Optional[Throttling] = None):
        self.throttling = throttling

    def send(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        raise NotImplementedError()
