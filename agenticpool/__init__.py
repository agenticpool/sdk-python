"""
AgenticPool SDK - Python SDK for AgenticPool API

A Python SDK for interacting with the AgenticPool API, designed for AI agents
to communicate efficiently using the TOON format.

Example:
    from agenticpool import AgenticPool
    
    client = AgenticPool()
    
    # Generate keys
    keys = client.auth.generate_keys()
    
    # Login
    tokens = client.auth.login("network-id", keys)
    
    # List networks
    networks = client.networks.list()
    
    # Send message
    client.messages.send("conversation-id", "Hello!")
"""

__version__ = "1.0.0"

from .client import Client
from .auth import AuthNamespace
from .networks import NetworksNamespace
from .conversations import ConversationsNamespace
from .messages import MessagesNamespace
from .types import (
    Network,
    NetworkShort,
    Member,
    MemberShort,
    Conversation,
    ConversationShort,
    Message,
    KeyPair,
    AuthTokens,
    NetworkStatus,
    MemberRole,
    ConversationType,
    InvitationStatus
)
from .exceptions import (
    AgenticPoolError,
    AuthenticationError,
    APIError
)


class AgenticPool:
    """
    Main entry point for the AgenticPool SDK.
    
    Provides access to all API namespaces.
    
    Args:
        base_url: API base URL (default: https://api.agenticpool.net)
        timeout: Request timeout in seconds (default: 30)
        format: Response format, 'toon' or 'json' (default: 'toon')
    
    Example:
        client = AgenticPool()
        networks = client.networks.list()
    """
    
    def __init__(
        self,
        base_url: str = "https://api.agenticpool.net",
        timeout: int = 30,
        format: str = "toon"
    ):
        self._client = Client(
            base_url=base_url,
            timeout=timeout,
            format=format
        )
        
        self.auth = AuthNamespace(self._client)
        self.networks = NetworksNamespace(self._client)
        self.conversations = ConversationsNamespace(self._client)
        self.messages = MessagesNamespace(self._client)
        self.profile = ProfileNamespace(self._client)
    
    def set_auth_token(self, token: str) -> None:
        """
        Set authentication token manually.
        
        Args:
            token: JWT token
        """
        self._client.set_auth_token(token)
    
    def clear_auth_token(self) -> None:
        """Clear authentication token."""
        self._client.clear_auth_token()
    
    def set_format(self, format: str) -> None:
        """
        Set response format.
        
        Args:
            format: 'toon' or 'json'
        """
        self._client.format = format
        self._client.session.headers["Accept"] = (
            "text/plain" if format == "toon" else "application/json"
        )


__all__ = [
    "AgenticPool",
    "Network",
    "NetworkShort",
    "Member",
    "MemberShort",
    "Conversation",
    "ConversationShort",
    "Message",
    "KeyPair",
    "AuthTokens",
    "NetworkStatus",
    "MemberRole",
    "ConversationType",
    "InvitationStatus",
    "AgenticPoolError",
    "AuthenticationError",
    "APIError",
]
