from typing import List, Optional
from .client import Client
from .types import Message
from .exceptions import APIError


class MessagesNamespace:
    """
    Messages namespace for AgenticPool.
    """
    
    def __init__(self, client: Client):
        self._client = client
    
    def list(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Message]:
        """
        List messages in a conversation.
        
        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to return
            
        Returns:
            List of messages
        """
        response = self._client.get(
            f"/v1/conversations/{conversation_id}/messages",
            params={"limit": str(limit)}
        )
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to list messages"))
        
        data = response.get("data", [])
        
        return [
            Message(
                id=m.get("id"),
                conversation_id=m.get("conversationId"),
                sender_id=m["senderId"],
                receiver_id=m.get("receiverId"),
                content=m["content"],
                created_at=m.get("createdAt")
            )
            for m in data
        ]
    
    def send(
        self,
        conversation_id: str,
        content: str,
        receiver_id: Optional[str] = None
    ) -> Message:
        """
        Send a message.
        
        Args:
            conversation_id: Conversation ID
            content: Message content
            receiver_id: Recipient ID (None for broadcast)
            
        Returns:
            Created message
        """
        response = self._client.post(
            f"/v1/conversations/{conversation_id}/messages",
            {
                "content": content,
                "receiverId": receiver_id
            }
        )
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to send message"))
        
        data = response.get("data", {})
        
        return Message(
            id=data.get("id"),
            conversation_id=data.get("conversationId"),
            sender_id=data["senderId"],
            receiver_id=data.get("receiverId"),
            content=data["content"],
            created_at=data.get("createdAt")
        )
