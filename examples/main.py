import logging
import os
import time

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
    time.sleep(2)
    raise Exception("test")


if __name__ == "__main__":
    main()
