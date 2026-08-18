"""
Heysender Python SDK
====================

Official Python SDK for the Heysender API.

"""

from .hs_client import HeysenderClient
from .message_builder import MessageBuilder
from .hs_exception import HeysenderException
from .enums import AnonymizeOption, EventType, SuppressionType

__version__ = "0.9.1"
__author__ = "Heysender ApS"
__email__ = "contact@heysender.com"
__license__ = "MIT"

__all__ = [
    "HeysenderClient",
    "MessageBuilder",
    "HeysenderException",
    "AnonymizeOption",
    "EventType",
    "SuppressionType",
]
