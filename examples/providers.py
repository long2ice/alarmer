from typing import Optional


def my_provider(message: str, exc: Optional[BaseException] = None):
    print(f"send {message} success")
