import abc
import threading
import time
import typing

if typing.TYPE_CHECKING:
    from alarmer import Provider


class Throttling(abc.ABC):
    def __init__(self):
        self.last_time = time.time()
        self.lock = threading.Lock()

    def __call__(self, provider: "Provider", message: str) -> bool:
        with self.lock:
            if time.time() - self.last_time < 1:
                return False
            self.last_time = time.time()
            return True
