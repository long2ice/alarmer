import abc
import json
from typing import Optional

from alarmer.encoder import ComplexEncoder
from alarmer.throttling import Throttling


class Provider(abc.ABC):
    def __init__(self, throttling: Optional[Throttling] = None):
        self.throttling = throttling

    def build_message(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        if context:
            message = (
                message
                + f'{"-" * 100}\nContext Variables:\n'
                + json.dumps(context, indent=4, cls=ComplexEncoder)
            )
        return message

    def send(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        raise NotImplementedError
