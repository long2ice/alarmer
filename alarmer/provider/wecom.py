import requests

from alarmer import Provider


class WeComProvider(Provider):
    """
    https://work.weixin.qq.com/api/doc/90000/90136/91770
    """

    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def send(self, message: str):
        data = {"msgtype": "text", "content": {"text": message}}
        return requests.post(
            self.webhook_url,
            json=data,
        )
