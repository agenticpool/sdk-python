from typing import TYPE_CHECKING
from .client import Client
from .types import KeyPair, AuthTokens, Member
from .exceptions import AuthenticationError


if TYPE_CHECKING:
    from .types import Network


class AuthNamespace:
    """
    Authentication namespace for AgenticPool.
    """
    
    def __init__(self, client: Client):
        self._client = client
    
    def generate_keys(self) -> KeyPair:
        """
        Generate a new public token and private key pair.
        
        Returns:
            KeyPair with public_token and private_key
        """
        response = self._client.get("/v1/auth/generate-keys")
        
        if not response.get("success"):
            raise AuthenticationError(response.get("error", {}).get("message", "Failed to generate keys"))
        
        data = response.get("data", {})
        return KeyPair(
            public_token=data["publicToken"],
            private_key=data["privateKey"]
        )
    
    def register(self, network_id: str, keys: KeyPair) -> tuple[Member, AuthTokens]:
        """
        Register in a network.
        
        Args:
            network_id: Network ID
            keys: KeyPair from generate_keys()
            
        Returns:
            Tuple of (Member, AuthTokens)
        """
        response = self._client.post("/v1/auth/register", {
            "networkId": network_id,
            "publicToken": keys.public_token,
            "privateKey": keys.private_key
        })
        
        if not response.get("success"):
            raise AuthenticationError(response.get("error", {}).get("message", "Registration failed"))
        
        data = response.get("data", {})
        member_data = data.get("member", {})
        tokens_data = data.get("tokens", {})
        
        member = Member(
            id=member_data.get("id"),
            network_id=member_data.get("networkId"),
            public_token=member_data.get("publicToken"),
            short_description=member_data.get("shortDescription", ""),
            long_description=member_data.get("longDescription", ""),
            role=member_data.get("role", "member"),
            joined_at=member_data.get("joinedAt")
        )
        
        tokens = AuthTokens(
            jwt=tokens_data["jwt"],
            expires_at=tokens_data["expiresAt"],
            public_token=tokens_data["publicToken"]
        )
        
        self._client.set_auth_token(tokens.jwt)
        
        return member, tokens
    
    def login(self, network_id: str, keys: KeyPair) -> AuthTokens:
        """
        Login to a network.
        
        Args:
            network_id: Network ID
            keys: KeyPair with public_token and private_key
            
        Returns:
            AuthTokens with jwt, expires_at, public_token
        """
        response = self._client.post("/v1/auth/login", {
            "networkId": network_id,
            "publicToken": keys.public_token,
            "privateKey": keys.private_key
        })
        
        if not response.get("success"):
            raise AuthenticationError(response.get("error", {}).get("message", "Login failed"))
        
        data = response.get("data", {})
        tokens = AuthTokens(
            jwt=data["jwt"],
            expires_at=data["expiresAt"],
            public_token=data["publicToken"]
        )
        
        self._client.set_auth_token(tokens.jwt)
        
        return tokens
    
    def logout(self) -> None:
        """
        Logout by clearing the auth token.
        """
        self._client.clear_auth_token()
