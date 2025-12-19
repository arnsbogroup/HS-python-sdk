from enum import Enum
from typing import List


class SuppressionType(Enum):

    BOUNCES = "bounce"
    UNSUBSCRIBES = "unsubscribe"
    COMPLAINTS = "complaint"

    @classmethod
    def values(cls) -> List[str]:
        return [suppression.value for suppression in cls]

    def __str__(self) -> str:
        """String representation of the suppression type."""
        return self.value
