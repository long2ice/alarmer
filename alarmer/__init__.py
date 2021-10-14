import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional, Union

import better_exceptions  # type:ignore

from alarmer.provider import Provider
from alarmer.throttling import Throttling


class Alarmer:
    _old_except_hook: Callable
    _providers: List[Union[Provider, Callable]]
    _pool: ThreadPoolExecutor
    _global_throttling: Optional[Throttling]
    environment: str

    @classmethod
    def except_hook(cls, exc, value, tb):
        context = None
        if tb is not None:
            prev = tb
            curr = tb.tb_next
            while curr is not None:
                prev = curr
                curr = curr.tb_next
            context = prev.tb_frame.f_locals
        cls._old_except_hook(exc, value, tb)
        message = "".join(better_exceptions.format_exception(exc, value, tb))
        cls.send(message, exc, context)

    @classmethod
    def send(
        cls, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        for p in cls._providers:
            if isinstance(p, Provider):
                t = p.throttling or cls._global_throttling
                if (t and t(p, message, exc, context)) or not t:
                    cls._pool.submit(p.send, message, exc, context)
            else:
                if cls._global_throttling and cls._global_throttling(p, message, exc, context):
                    cls._pool.submit(p, message, exc, context)

    @classmethod
    def init(
        cls,
        providers: List[Union[Provider, Callable]],
        thread_pool_size: Optional[int] = None,
        global_throttling: Optional[Throttling] = Throttling(),
        environment: str = "production",
    ):
        better_exceptions.MAX_LENGTH = None
        cls._global_throttling = global_throttling
        cls._old_except_hook = sys.excepthook
        cls.environment = environment
        cls._providers = providers
        sys.excepthook = cls.except_hook
        cls._pool = ThreadPoolExecutor(max_workers=thread_pool_size)
