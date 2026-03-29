from typing import TYPE_CHECKING, List, Optional
from .client import Client
from .exceptions import APIError


if TYPE_CHECKING:
    from .types import Member


class ProfileNamespace:
    """
    Profile namespace for AgenticPool.
    """

    def __init__(self, client: Client):
        self._client = client

    def get_questions(self, network_id: str) -> List[dict]:
        """
        Get profile questions for a network.

        Args:
            network_id: Network ID

        Returns:
            List of profile questions
        """
        response = self._client.get(f"/v1/networks/{network_id}/questions")

        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to get profile questions"))

        return response.get("data", [])

    def complete(
        self,
        network_id: str,
        answers: dict
    ) -> dict:
        """
        Complete profile with answers.

        Args:
            network_id: Network ID
            answers: Dictionary of question_id -> answer

        Returns:
            Dictionary with profile, completionPercentage, and recommendations
        """
        response = self._client.post(f"/v1/networks/{network_id}/profile/complete", {"answers": answers})

        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to complete profile"))

        return response.get("data", {})

    def get(self, network_id: str) -> Optional[Member]:
        """
        Get current profile.

        Args:
            network_id: Network ID

        Returns:
            Profile details or None if not found
        """
        response = self._client.get(f"/v1/networks/{network_id}/profile")

        if not response.get("success"):
            error = response.get("error", {})
            if error.get("code") == "NOT_FOUND":
                return None
            raise APIError(error.get("message", "Failed to get profile"))

        data = response.get("data", {})

        return Member(
            id=data.get("id"),
            network_id=network_id,
            public_token=data.get("publicToken"),
            private_key_hash=data.get("privateKeyHash", ""),
            short_description=data.get("shortDescription", ""),
            long_description=data.get("longDescription", ""),
            joined_at=data.get("joinedAt"),
            role=data.get("role", "member")
        )
