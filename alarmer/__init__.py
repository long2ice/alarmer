import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional

import better_exceptions  # type:ignore

from alarmer.provider import Provider
from alarmer.throttling import Throttling


class Alarmer:
    _old_except_hook: Callable
    _providers: List[Provider]
    _pool: ThreadPoolExecutor
    _global_throttling: Optional[Throttling]

    @classmethod
    def except_hook(cls, exc, value, tb):
        cls._old_except_hook(exc, value, tb)
        message = "".join(better_exceptions.format_exception(exc, value, tb))
        cls.send(message)

    @classmethod
    def send(cls, message: str):
        for p in cls._providers:
            t = p.throttling or cls._global_throttling
            if t and t(p, message):
                cls._pool.submit(p.send, message)

    @classmethod
    def init(
        cls,
        providers: List[Provider],
        thread_pool_size: Optional[int] = None,
        global_throttling: Throttling = Throttling(),
    ):
        cls._pool = ThreadPoolExecutor(max_workers=thread_pool_size)
        cls._global_throttling = global_throttling
        cls._old_except_hook = sys.excepthook
        cls._providers = providers
        sys.excepthook = cls.except_hook
