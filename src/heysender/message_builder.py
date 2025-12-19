from typing import Dict, List, Optional, Union

from .enums import AnonymizeOption, EventType


class MessageBuilder:

    def __init__(self, from_email: str, from_name: str, subject: str, html: str):
        """
        Initialize message builder

        Args:
            from_email: Sender email address
            from_name: Sender name
            subject: Email subject
            html: HTML body content
        """
        self.data = {
            "from_email": from_email,
            "from_name": from_name,
            "subject": subject,
            "html": html
        }

    def set_text(self, text: str) -> 'MessageBuilder':
        """Set plain text body"""
        self.data["text"] = text
        return self

    def add_to(self, email: str, name: Optional[str] = None) -> 'MessageBuilder':
        """
        Add TO recipient

        Args:
            email: Recipient email
            name: Recipient name (optional)
        """
        if "to" not in self.data:
            self.data["to"] = []

        recipient = {"email": email}
        if name:
            recipient["name"] = name

        self.data["to"].append(recipient)
        return self

    def add_cc(self, email: str, name: Optional[str] = None) -> 'MessageBuilder':
        """
        Add CC recipient

        Args:
            email: Recipient email
            name: Recipient name (optional)
        """
        if "cc" not in self.data:
            self.data["cc"] = []

        recipient = {"email": email}
        if name:
            recipient["name"] = name

        self.data["cc"].append(recipient)
        return self

    def add_bcc(self, email: str) -> 'MessageBuilder':
        """
        Add BCC recipient

        Args:
            email: Recipient email
        """
        if "bcc" not in self.data:
            self.data["bcc"] = []

        self.data["bcc"].append(email)
        return self

    def set_reply_to(self, reply_to: Union[str, List[Dict]]) -> 'MessageBuilder':
        """
        Set reply-to address(es)

        Args:
            reply_to: Single email string or list of email/name dicts
        """
        self.data["reply_to"] = reply_to
        return self

    def add_attachment(self, name: str, base64_content: str) -> 'MessageBuilder':
        """
        Add attachment

        Args:
            name: Filename with extension
            base64_content: Base64 encoded file content
        """
        if "attachments" not in self.data:
            self.data["attachments"] = []

        self.data["attachments"].append({
            "name": name,
            "content": base64_content
        })
        return self

    def add_tag(self, key: str, value: str) -> 'MessageBuilder':
        """
        Add custom tag

        Args:
            key: Tag key
            value: Tag value
        """
        if "tags" not in self.data:
            self.data["tags"] = []

        self.data["tags"].append({
            "key": key,
            "value": value
        })
        return self

    def add_header(self, key: str, value: str) -> 'MessageBuilder':
        """
        Add custom header

        Args:
            key: Header key
            value: Header value
        """
        if "headers" not in self.data:
            self.data["headers"] = []

        self.data["headers"].append({
            "key": key,
            "value": value
        })
        return self

    def set_custom_content(self, custom_content: Dict[str, Dict]) -> 'MessageBuilder':
        """
        Set custom content for bulk messaging

        Args:
            custom_content: Dict mapping recipient emails to custom variables
        """
        self.data["custom_content"] = custom_content
        return self

    def set_tracking(self, enabled: bool) -> 'MessageBuilder':
        """
        Enable/disable open and click tracking

        Args:
            enabled: Whether to enable tracking
        """
        self.data["tracking"] = enabled
        return self

    def set_list_unsubscribe(self, enabled: bool) -> 'MessageBuilder':
        """
        Enable/disable list-unsubscribe header

        Args:
            enabled: Whether to enable list-unsubscribe
        """
        self.data["list_unsubscribe"] = enabled
        return self

    def set_retention_time(self, days: int) -> 'MessageBuilder':
        """
        Set message retention time in days

        Args:
            days: Number of days to retain message
        """
        self.data["retention_time"] = days
        return self

    def set_anonymize_options(self, options: List[Union[AnonymizeOption, str]]) -> 'MessageBuilder':
        """
        Set anonymization options

        Args:
            options: List of fields to anonymize (use AnonymizeOption enum or strings)
        """
        # Convert enums to strings if needed
        options_list = [
            opt.value if isinstance(opt, AnonymizeOption) else opt
            for opt in options
        ]
        self.data["anonymize_options"] = options_list
        return self

    def set_webhook(self, url: str, events: List[Union[EventType, str]]) -> 'MessageBuilder':
        """
        Set custom webhook for this message

        Args:
            url: Webhook URL
            events: List of events to trigger webhook (use EventType enum or strings)
        """
        # Convert enums to strings if needed
        event_strings = [
            event.value if isinstance(event, EventType) else event
            for event in events
        ]
        self.data["webhook"] = {
            "url": url,
            "events": event_strings
        }
        return self

    def build(self) -> Dict:
        """
        Build and return the message data dictionary

        Returns:
            Complete message data dict
        """
        return self.data
