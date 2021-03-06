import logging
import os

from alarmer import Alarmer
from alarmer.log import LoggingHandler
from alarmer.provider.feishu import FeiShuProvider
from examples.providers import my_provider


def main():
    Alarmer.init(
        providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL")), my_provider],
        global_throttling=None,
    )
    logging.basicConfig(
        level=logging.INFO,
    )
    logger = logging.getLogger()
    logger.addHandler(LoggingHandler())
    logging.error("test logging")
    a = 1
    b = 0
    a / b


if __name__ == "__main__":
    main()
