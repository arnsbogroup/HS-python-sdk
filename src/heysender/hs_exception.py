from typing import Optional


class HeysenderException(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        """
        Initialize a Heysender exception.

        Args:
            message: Error message
            status_code: HTTP status code (optional)
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"HeysenderException ({self.status_code}): {self.message}"
        return f"HeysenderException: {self.message}"
