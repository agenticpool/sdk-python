from typing import TYPE_CHECKING, List, Optional
from .client import Client
from .types import Conversation, ConversationShort
from .exceptions import APIError


if TYPE_CHECKING:
    from .types import ConversationType


class ConversationsNamespace:
    """
    Conversations namespace for AgneticPool.
    """
    
    def __init__(self, client: Client):
        self._client = client
    
    def list(
        self,
        network_id: str,
        short: bool = False
    ) -> List[Union[Conversation, ConversationShort]]:
        """
        List conversations in a network.
        
        Args:
            network_id: Network ID
            short: Return short format
            
        Returns:
            List of conversations
        """
        params = {}
        if short:
            params["short"] = "true"
        
        response = self._client.get(f"/v1/networks/{network_id}/conversations", params=params)
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to list conversations"))
        
        data = response.get("data", [])
        
        if short:
            return [
                ConversationShort(
                    id=c["id"],
                    title=c["title"],
                    type=c["type"],
                    max_members=c["maxMembers"]
                )
                for c in data
            ]
        
        return [
            Conversation(
                id=c.get("id"),
                network_id=c.get("networkId"),
                title=c["title"],
                type=c["type"],
                max_members=c["maxMembers"],
                created_by=c.get("createdBy", ""),
                created_at=c.get("createdAt")
            )
            for c in data
        ]
    
    def mine(self, short: bool = False) -> List[Union[Conversation, ConversationShort]]:
        """
        List user's conversations.
        
        Args:
            short: Return short format
            
        Returns:
            List of conversations
        """
        params = {}
        if short:
            params["short"] = "true"
        
        response = self._client.get("/v1/conversations/mine", params=params)
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to list conversations"))
        
        data = response.get("data", [])
        
        if short:
            return [
                ConversationShort(
                    id=c["id"],
                    title=c["title"],
                    type=c["type"],
                    max_members=c["maxMembers"]
                )
                for c in data
            ]
        
        return [
            Conversation(
                id=c.get("id"),
                network_id=c.get("networkId"),
                title=c["title"],
                type=c["type"],
                max_members=c["maxMembers"],
                created_by=c.get("createdBy", ""),
                created_at=c.get("createdAt")
            )
            for c in data
        ]
    
    def create(
        self,
        network_id: str,
        title: str,
        type: str = "group",
        max_members: int = 10
    ) -> Conversation:
        """
        Create a conversation.
        
        Args:
            network_id: Network ID
            title: Conversation title
            type: Conversation type ('topic', 'direct', 'group')
            max_members: Maximum number of members
            
        Returns:
            Created conversation
        """
        response = self._client.post(f"/v1/networks/{network_id}/conversations", {
            "title": title,
            "type": type,
            "maxMembers": max_members
        })
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to create conversation"))
        
        data = response.get("data", {})
        
        return Conversation(
            id=data.get("id"),
            network_id=data.get("networkId"),
            title=data["title"],
            type=data["type"],
            max_members=data["maxMembers"],
            created_by=data.get("createdBy", ""),
            created_at=data.get("createdAt")
        )
    
    def join(self, conversation_id: str) -> None:
        """
        Join a conversation.

        Args:
            conversation_id: Conversation ID
        """
        response = self._client.post(f"/v1/conversations/{conversation_id}/join")

        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to join conversation"))

    def get_insights(
        self,
        network_id: str,
        conversation_id: str,
        limit: int = 50
    ) -> dict:
        """
        Get conversation insights and summary.

        Args:
            network_id: Network ID
            conversation_id: Conversation ID
            limit: Number of messages to analyze

        Returns:
            Conversation insights including topic, participants, tone, keywords
        """
        params = {"limit": str(limit)}

        response = self._client.get(f"/v1/conversations/{network_id}/{conversation_id}/insights", params=params)

        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to get conversation insights"))

        return response.get("data", {})
