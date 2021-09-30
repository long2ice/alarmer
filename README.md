# alerter

[![image](https://img.shields.io/pypi/v/alerter.svg?style=flat)](https://pypi.python.org/pypi/alerter)
[![image](https://img.shields.io/github/license/tortoise/alerter)](https://github.com/tortoise/alerter)
[![image](https://github.com/tortoise/alerter/workflows/pypi/badge.svg)](https://github.com/tortoise/alerter/actions?query=workflow:pypi)
[![image](https://github.com/tortoise/alerter/workflows/ci/badge.svg)](https://github.com/tortoise/alerter/actions?query=workflow:ci)

`Alerter` is a tool focus on error reporting for your application.

## Installation

```shell
pip install alerter
```

## Usage

It's simple to integrate `alerter` in your application, just call `Alerter.init` on startup of your application.

```py
import os

from alerter import Alerter
from alerter.provider.feishu import FeiShuProvider


def main():
    Alerter.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])
    raise Exception("test")


if __name__ == "__main__":
    main()
```

### Intercept Error Logging

If you want to intercept the `ERROR` level logging, you can use `LoggingHandler`.

```py
import logging
import os

from alerter import Alerter
from alerter.log import LoggingHandler
from alerter.provider.feishu import FeiShuProvider


def main():
    Alerter.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])
    logging.basicConfig(
        level=logging.INFO,
    )
    logger = logging.getLogger()
    logger.addHandler(LoggingHandler())
    logging.error("test logging")


if __name__ == "__main__":
    main()

```

Now when you run the script, you will receive the errors in your provider.

## Provider

You can set number of providers for error reporting. All kinds of providers can be found
in [providers](./alerter/provider).

- Email
- [FeiShu](https://www.feishu.cn/hc/zh-CN/articles/360024984973)
- [WeCom](https://work.weixin.qq.com/api/doc/90000/90136/91770)

### Custom Provider

You can write your own custom provider by inheriting the `Provider` class.

```py
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
```

## Throttling

`Throttling` is used to throttle error messages.

```py
from alerter import Alerter
from alerter.throttling import Throttling

Alerter.init(global_throttling=Throttling(), providers=[...])
```

### Custom Throttling

You can write your own throttling by inheriting the `Throttling` class.

```py
import abc
import threading
import time
import typing

if typing.TYPE_CHECKING:
    from alerter import Provider


class Throttling(abc.ABC):
    def __init__(self):
        self.last_time = time.time()
        self.lock = threading.Lock()

    def __call__(self, provider: "Provider", exc, value, tb) -> bool:
        with self.lock:
            if time.time() - self.last_time < 1:
                return False
            self.last_time = time.time()
            return True

```

## License

This project is licensed under the
[Apache-2.0](https://github.com/long2ice/alerter/blob/master/LICENSE) License.
