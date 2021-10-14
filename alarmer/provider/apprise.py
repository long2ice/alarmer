from typing import List, Optional

import apprise

from alarmer import Alarmer, Throttling
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

    def send(
        self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None
    ):
        title = (
            f"[{Alarmer.environment}] Exception Alarm: {exc}"
            if exc
            else f"[{Alarmer.environment}] Alarm"
        )

        return self.app.notify(title=title, body=message, **self.notify_options)
