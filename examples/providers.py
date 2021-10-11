from typing import Optional


def my_provider(message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None):
    print(f"send {message} success")
