from enum import Enum
from typing import List


class AnonymizeOption(Enum):

    NONE = "none"
    ALL = "all"
    RECIPIENT = "recipient"
    SUBJECT = "subject"
    CONTENT = "content"

    @classmethod
    def values(cls) -> List[str]:
        return [option.value for option in cls]

    def __str__(self) -> str:
        """String representation of the anonymization option."""
        return self.value
