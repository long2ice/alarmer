from typing import Optional

import requests

from alarmer import Provider, Throttling


class WeComProvider(Provider):
    """
    https://work.weixin.qq.com/api/doc/90000/90136/91770
    """

    def __init__(
        self,
        webhook_url: str,
        throttling: Optional[Throttling] = None,
    ):
        super().__init__(throttling)
        self.webhook_url = webhook_url

    def send(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        data = {"msgtype": "text", "content": {"text": message}}
        return requests.post(
            self.webhook_url,
            json=data,
        )
