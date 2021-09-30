# alarmer

[![image](https://img.shields.io/pypi/v/alarmer.svg?style=flat)](https://pypi.python.org/pypi/alarmer)
[![image](https://img.shields.io/github/license/tortoise/alarmer)](https://github.com/tortoise/alarmer)
[![pypi](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml)
[![ci](https://github.com/long2ice/alarmer/actions/workflows/ci.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/ci.yml)

`Alarmer` is a tool focus on error reporting for your application.

## Installation

```shell
pip install alarmer
```

## Usage

It's simple to integrate `alarmer` in your application, just call `Alarmer.init` on startup of your application.

```py
import os

from alarmer import Alarmer
from alarmer.provider.feishu import FeiShuProvider


def main():
    Alarmer.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])
    raise Exception("test")


if __name__ == "__main__":
    main()
```

### Intercept Error Logging

If you want to intercept the `ERROR` level logging, you can use `LoggingHandler`.

```py
import logging
import os

from alarmer import Alarmer
from alarmer.log import LoggingHandler
from alarmer.provider.feishu import FeiShuProvider


def main():
    Alarmer.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])
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
in [providers](./alarmer/provider).

- Email
- [FeiShu](https://www.feishu.cn/hc/zh-CN/articles/360024984973)
- [WeCom](https://work.weixin.qq.com/api/doc/90000/90136/91770)

### Custom Provider

You can write your own custom provider by inheriting the `Provider` class.

```py
import smtplib
from typing import List

from alarmer.provider import Provider


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

`Throttling` is used to throttling error messages if there are too many errors.

```py
from alarmer import Alarmer
from alarmer.throttling import Throttling

Alarmer.init(global_throttling=Throttling(), providers=[...])
```

### Custom Throttling

You can write your own throttling by inheriting the `Throttling` class.

```py
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
```

## License

This project is licensed under the
[Apache-2.0](https://github.com/long2ice/alarmer/blob/master/LICENSE) License.
