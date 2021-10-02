import requests

from alarmer import Provider


class FeiShuProvider(Provider):
    """
    https://www.feishu.cn/hc/zh-CN/articles/360024984973
    """

    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def send(self, message: str):
        data = {"msg_type": "text", "content": {"text": message}}
        return requests.post(
            self.webhook_url,
            json=data,
        )
