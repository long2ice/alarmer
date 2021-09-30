import smtplib
from typing import List

from alerter.provider import Provider


class EmailProvider(Provider):
    def __init__(self, host: str, port: int, from_addr: str, to_addrs: List[str], **kwargs):
        super().__init__()
        self.smtp = smtplib.SMTP(host=host, port=port)
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.kwargs = kwargs

    def send(self, message: str):
        self.smtp.sendmail(
            from_addr=self.from_addr, to_addrs=self.to_addrs, msg=message, **self.kwargs
        )
