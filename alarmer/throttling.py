import threading
import time
import typing

if typing.TYPE_CHECKING:
    from alarmer import Provider


class Throttling:
    def __init__(self):
        self.last_time = time.time()
        self.lock = threading.Lock()

    def __call__(
        self,
        provider: "typing.Union[Provider,typing.Callable]",
        message: str,
        exc: typing.Optional[BaseException] = None,
        context: typing.Optional[dict] = None,
    ) -> bool:
        with self.lock:
            if time.time() - self.last_time < 5:
                return False
            self.last_time = time.time()
            return True
