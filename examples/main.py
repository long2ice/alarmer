import logging
import os
import time

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
    time.sleep(2)
    raise Exception("test")


if __name__ == "__main__":
    main()
