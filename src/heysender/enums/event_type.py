from enum import Enum
from typing import List


class EventType(Enum):

    QUEUED = "queued"
    SENT = "sent"
    ATTEMPT = "attempt"
    SOFT_BOUNCE = "soft_bounce"
    HARD_BOUNCE = "hard_bounce"
    COMPLAINT = "complaint"
    UNSUBSCRIBE = "unsubscribe"
    OPEN = "open"
    CLICK = "click"

    @classmethod
    def values(cls) -> List[str]:
        return [event.value for event in cls]

    def __str__(self) -> str:
        """String representation of the event type."""
        return self.value
