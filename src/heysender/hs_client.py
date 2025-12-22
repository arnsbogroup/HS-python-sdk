"""
Heysender API Client

Main client class for interacting with the Heysender API.
"""

import base64
from typing import Any, Dict, List, Union, Optional
import requests

from .hs_exception import HeysenderException
from .enums import AnonymizeOption, EventType, SuppressionType


class HeysenderClient:
    """
    Main client for interacting with the Heysender API

    Args:
        api_key: Your Heysender API key
        api_secret: Your Heysender API secret
        base_url: Base URL for the API (default: https://app.heysender.com)
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://app.heysender.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.last_response = None

        # Set up authentication
        credentials = f"{api_key}:{api_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update({
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Union[Dict, List]:
        """
        Make an HTTP request to the API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request data

        Returns:
            Response data as dict or list

        Raises:
            HeysenderException: If the request fails
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            else:
                raise HeysenderException(f"Unsupported HTTP method: {method}")

            self.last_response = response

            # Handle error responses
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_message = json.dumps(error_data)
                except:
                    error_message = response.text

                raise HeysenderException(
                    f"API Error ({response.status_code}): {error_message}",
                    response.status_code
                )

            # Return JSON response
            if response.text:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            raise HeysenderException(f"Request failed: {str(e)}")

    # ==================== DOMAIN METHODS ====================

    def get_domains(self) -> List[Dict]:
        """
        Get list of domains

        Returns:
            List of domain objects
        """
        return self._request("GET", "/api/domains")

    def create_domain(
        self,
        url: str,
        custom_selector: Optional[str] = None,
        dkim_key: Optional[str] = None
    ) -> Dict:
        """
        Create a new domain

        Args:
            url: Domain URL
            custom_selector: Custom DKIM selector (optional)
            dkim_key: Custom DKIM private key (optional)

        Returns:
            Created domain data
        """
        data = {"url": url}

        if custom_selector:
            data["custom_selector"] = custom_selector

        if dkim_key:
            data["dkim_key"] = dkim_key

        return self._request("POST", "/api/domains", data)

    def update_domain(self, domain: str, dkim_key: str) -> Dict:
        """
        Update domain with new DKIM key

        Args:
            domain: Domain name
            dkim_key: New DKIM private key

        Returns:
            Response data
        """
        return self._request("PUT", f"/api/domains/{domain}", {"dkim_key": dkim_key})

    def delete_domain(self, domain: str) -> Dict:
        """
        Delete a domain

        Args:
            domain: Domain name

        Returns:
            Response data
        """
        return self._request("DELETE", f"/api/domains/{domain}")

    def validate_domain(self, domain: str) -> Dict:
        """
        Validate domain SPF and DKIM

        Args:
            domain: Domain name

        Returns:
            Validation status including SPF and DKIM checks
        """
        return self._request("GET", f"/api/domains/{domain}/validate")

    # ==================== SMTP USER METHODS ====================

    def get_smtp_users(self, domain_id: int) -> List[Dict]:
        """
        Get SMTP users for a domain

        Args:
            domain_id: Domain ID

        Returns:
            List of SMTP users
        """
        return self._request("GET", f"/api/smtp/{domain_id}")

    def create_smtp_user(
        self,
        domain_id: int,
        smtp_email: str,
        anonymize_options: List[Union[AnonymizeOption, str]] = None
    ) -> Dict:
        """
        Create SMTP user

        Args:
            domain_id: Domain ID
            smtp_email: SMTP email address
            anonymize_options: List of anonymization options (use AnonymizeOption enum or strings)

        Returns:
            Created SMTP user with password
        """
        if anonymize_options is None:
            anonymize_options = [AnonymizeOption.NONE]

        # Convert enums to strings if needed
        options_list = [
            opt.value if isinstance(opt, AnonymizeOption) else opt
            for opt in anonymize_options
        ]

        return self._request("POST", f"/api/smtp/{domain_id}", {
            "smtp_email": smtp_email,
            "anonymize_options": options_list
        })

    def delete_smtp_user(self, domain_id: int, user_id: int) -> Dict:
        """
        Delete SMTP user

        Args:
            domain_id: Domain ID
            user_id: SMTP user ID

        Returns:
            Response data
        """
        return self._request("DELETE", f"/api/smtp/{domain_id}/{user_id}")

    def reset_smtp_password(self, domain_id: int, user_id: int) -> Dict:
        """
        Generate new password for SMTP user

        Args:
            domain_id: Domain ID
            user_id: SMTP user ID

        Returns:
            New password data
        """
        return self._request("GET", f"/api/smtp/{domain_id}/{user_id}/newpassword")

    # ==================== WEBHOOK METHODS ====================

    def get_webhooks(self, domain: str) -> List[Dict]:
        """
        Get webhooks for a domain

        Args:
            domain: Domain name

        Returns:
            List of webhooks
        """
        return self._request("GET", f"/api/webhooks/{domain}")

    def get_webhook(self, domain: str, webhook_id: int) -> Dict:
        """
        Get specific webhook

        Args:
            domain: Domain name
            webhook_id: Webhook ID

        Returns:
            Webhook data
        """
        return self._request("GET", f"/api/webhooks/{domain}/{webhook_id}")

    def create_webhook(self, domain: str, url: str, events: List[Union[EventType, str]] = None) -> Dict:
        """
        Create webhook

        Args:
            domain: Domain name
            url: Webhook URL
            events: List of event triggers (use EventType enum or strings)

        Returns:
            Created webhook data
        """
        if events is None:
            events = []

        # Convert enums to strings if needed
        event_strings = [
            event.value if isinstance(event, EventType) else event
            for event in events
        ]

        available_events = EventType.values()

        data = {"url": url}
        for event in available_events:
            data[event] = event in event_strings

        return self._request("POST", f"/api/webhooks/{domain}", data)

    def update_webhook(
        self,
        domain: str,
        webhook_id: int,
        url: str,
        events: List[Union[EventType, str]] = None
    ) -> Dict:
        """
        Update webhook

        Args:
            domain: Domain name
            webhook_id: Webhook ID
            url: Webhook URL
            events: List of event triggers (use EventType enum or strings)

        Returns:
            Response data
        """
        if events is None:
            events = []

        # Convert enums to strings if needed
        event_strings = [
            event.value if isinstance(event, EventType) else event
            for event in events
        ]

        available_events = EventType.values()

        data = {"url": url}
        for event in available_events:
            data[event] = event in event_strings

        return self._request("PUT", f"/api/webhooks/{domain}/{webhook_id}", data)

    def delete_webhook(self, domain: str, webhook_id: int) -> Dict:
        """
        Delete webhook

        Args:
            domain: Domain name
            webhook_id: Webhook ID

        Returns:
            Response data
        """
        return self._request("DELETE", f"/api/webhooks/{domain}/{webhook_id}")

    # ==================== MESSAGE METHODS ====================

    def send_message(self, message_data: Dict) -> List[Dict]:
        """
        Send an email message

        Args:
            message_data: Message data dictionary

        Returns:
            List of message responses with status and message IDs
        """
        return self._request("POST", "/api/message", message_data)

    def get_message(self, message_id: str) -> Dict:
        """
        Get message information

        Args:
            message_id: Message ID

        Returns:
            Message information
        """
        return self._request("GET", f"/api/message/{message_id}")

    def get_message_by_recipient(self, message_id: str, recipient: str) -> Dict:
        """
        Get message information for specific recipient

        Args:
            message_id: Message ID
            recipient: Recipient email

        Returns:
            Message information
        """
        return self._request("GET", f"/api/message/{message_id}/{recipient}")

    # ==================== SUPPRESSION METHODS ====================

    def get_suppressions(self, domain: str, suppression_type: Union[SuppressionType, str]) -> Dict:
        """
        Get suppressions by domain and type

        Args:
            domain: Domain name
            suppression_type: Suppression type (use SuppressionType enum or string:
                            'bounce', 'unsubscribe', 'complaint')

        Returns:
            Paginated suppression list
        """
        # Convert enum to string if needed
        type_str = (
            suppression_type.value
            if isinstance(suppression_type, SuppressionType)
            else suppression_type
        )

        return self._request("GET", f"/api/suppressions/{domain}/{type_str}")

    def remove_bounce(self, domain: str, email: str) -> Dict:
        """
        Remove email from bounce suppressions

        Args:
            domain: Domain name
            email: Email address to remove

        Returns:
            Response data
        """
        return self._request("DELETE", f"/api/suppressions/{domain}/bounce/{email}")

    # ==================== HELPER METHODS ====================

    def get_last_response(self) -> Optional[requests.Response]:
        """
        Get last HTTP response object

        Returns:
            Last response object
        """
        return self.last_response
