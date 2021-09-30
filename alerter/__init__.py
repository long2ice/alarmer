from typing import List
import better_exceptions

from alerter.provider import Provider


def init(providers: List[Provider]):
    better_exceptions.MAX_LENGTH = None
    better_exceptions.hook()
