# alarmer

[![image](https://img.shields.io/pypi/v/alarmer.svg?style=flat)](https://pypi.python.org/pypi/alarmer)
[![image](https://img.shields.io/github/license/long2ice/alarmer)](https://github.com/long2ice/alarmer)
[![pypi](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml)
[![ci](https://github.com/long2ice/alarmer/actions/workflows/ci.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/ci.yml)

`Alarmer` is a tool focus on error reporting for your application, like [sentry](https://sentry.io) but lightweight.

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

If you want to intercept the logging, you can use `LoggingHandler`.

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
    logger.addHandler(LoggingHandler(level=logging.ERROR))  # only error and above should be send
    logging.error("test logging")


if __name__ == "__main__":
    main()

```

Now when you run the script, you will receive the errors in your provider.

## Provider

You can set number of providers for error reporting. All kinds of providers can be found
in [providers](./alarmer/provider).

Thanks to [Apprise](https://github.com/caronc/apprise), you can use lots of providers out of box.

- [Apprise](https://github.com/caronc/apprise)
- [FeiShu](https://www.feishu.cn/hc/zh-CN/articles/360024984973)
- [WeCom](https://work.weixin.qq.com/api/doc/90000/90136/91770)

### Custom Provider

You can write your own custom provider by inheriting the `Provider` class.

```py
from typing import Optional
from alarmer.provider import Provider


class CustomProvider(Provider):

    def send(self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None):
        # Send to your custom provider here
        pass
```

In addition to this, you can just write a callable function which takes `message` and `exc` arguments.

```py
from typing import Optional


def custom_provider(message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None):
    # Send to your custom provider here
    pass
```

Then add it to `Alarmer.init`.

```py
from alarmer import Alarmer

Alarmer.init(providers=[CustomProvider(), custom_provider])
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
import typing

from alarmer.throttling import Throttling

if typing.TYPE_CHECKING:
    from alarmer.provider import Provider


class MyThrottling(Throttling):
    def __call__(self, provider: "typing.Union[Provider,typing.Callable]", message: str,
                 exc: typing.Optional[BaseException] = None, context: typing.Optional[dict] = None) -> bool:
        # check whether the error message should be send
        return True
```

## Manual Send

If you want to manually send messages to the providers, just call `Alarmer.send`.

```py
from alarmer import Alarmer

Alarmer.send("message")
```

## License

This project is licensed under the
[Apache-2.0](https://github.com/long2ice/alarmer/blob/master/LICENSE) License.
