import json
from typing import Optional

import requests

from alarmer import Alarmer, Provider, Throttling
from alarmer.encoder import ComplexEncoder


class FeiShuProvider(Provider):
    """
    https://www.feishu.cn/hc/zh-CN/articles/360024984973
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
        data: dict = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "content": f"[{Alarmer.environment}] Exception Alarm: {exc}"
                        if exc
                        else f"[{Alarmer.environment}] Alarm",
                        "tag": "plain_text",
                    },
                    "template": "red",
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {"content": message, "tag": "plain_text"},
                    },
                ],
            },
        }
        if context:
            context_content = json.dumps(context, indent=4, cls=ComplexEncoder)
            data["card"]["elements"].extend(
                [
                    {"tag": "hr"},
                    {
                        "tag": "div",
                        "fields": [
                            {
                                "is_short": True,
                                "text": {"tag": "lark_md", "content": "**Context Variables:**"},
                            },
                            {
                                "is_short": False,
                                "text": {"tag": "plain_text", "content": context_content},
                            },
                        ],
                    },
                ]
            )
        return requests.post(
            self.webhook_url,
            json=data,
        )
