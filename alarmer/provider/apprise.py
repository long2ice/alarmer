from typing import List, Optional

import apprise

from alarmer import Throttling
from alarmer.provider import Provider


class AppriseProvider(Provider):
    def __init__(
        self,
        services: List[str],
        throttling: Optional[Throttling] = None,
        apprise_options: Optional[dict] = None,
        notify_options: Optional[dict] = None,
    ):
        super().__init__(throttling)
        self.app = apprise.Apprise(services, **(apprise_options or {}))
        self.notify_options = notify_options or {}

    def send(self, message: str):
        return self.app.notify(body=message, **self.notify_options)
