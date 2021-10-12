import json
from typing import Optional

import requests

from alarmer import Provider, Throttling
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
        context_content = json.dumps(context, indent=4, cls=ComplexEncoder)
        data: dict = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "content": [
                            [
                                {"tag": "text", "text": message},
                                {"tag": "text", "text": "Context Variables:\n"},
                                {"tag": "text", "text": context_content},
                            ]
                        ],
                    },
                    "en_us": {
                        "content": [
                            [
                                {"tag": "text", "text": message},
                                {"tag": "text", "text": "上下文变量：\n"},
                                {"tag": "text", "text": context_content},
                            ]
                        ],
                    },
                }
            },
        }
        if exc:
            data["content"]["post"]["zh_cn"]["title"] = f"异常告警：{exc}"
            data["content"]["post"]["en_us"]["title"] = f"Exception Alarm: {exc}"
        return requests.post(
            self.webhook_url,
            json=data,
        )
