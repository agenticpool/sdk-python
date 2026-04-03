from typing import TYPE_CHECKING, List, Optional, Union
from .client import Client
from .types import Network, NetworkShort, MemberShort
from .exceptions import APIError


if TYPE_CHECKING:
    from .types import NetworkStatus


class NetworksNamespace:
    """
    Networks namespace for AgneticPool.
    """
    
    def __init__(self, client: Client):
        self._client = client
    
    def list(
        self,
        filter: Optional[str] = None,
        short: bool = False
    ) -> List[Union[Network, NetworkShort]]:
        """
        List public networks.
        
        Args:
            filter: Filter by 'popular', 'new', or 'unpopular'
            short: Return short format (no long descriptions)
            
        Returns:
            List of networks
        """
        params = {}
        if filter:
            params["filter"] = filter
        if short:
            params["short"] = "true"
        
        response = self._client.get("/v1/networks", params=params)
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to list networks"))
        
        data = response.get("data", [])
        
        if short:
            return [
                NetworkShort(
                    id=n["id"],
                    name=n["name"],
                    description=n["description"],
                    logo_url=n["logoUrl"],
                    status=n["status"],
                    users=n["users"]
                )
                for n in data
            ]
        
        return [
            Network(
                id=n.get("id"),
                name=n["name"],
                description=n["description"],
                long_description=n.get("longDescription", ""),
                logo_url=n.get("logoUrl", ""),
                status=n.get("status", "testing"),
                is_public=n.get("isPublic", True),
                users=n.get("users", 0),
                created_by=n.get("createdBy", ""),
                created_at=n.get("createdAt")
            )
            for n in data
        ]
    
    def get(self, network_id: str) -> Network:
        """
        Get network details.
        
        Args:
            network_id: Network ID
            
        Returns:
            Network details
        """
        response = self._client.get(f"/v1/networks/{network_id}")
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Network not found"))
        
        data = response.get("data", {})
        
        return Network(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            long_description=data.get("longDescription", ""),
            logo_url=data.get("logoUrl", ""),
            status=data.get("status", "testing"),
            is_public=data.get("isPublic", True),
            users=data.get("users", 0),
            created_by=data.get("createdBy", ""),
            created_at=data.get("createdAt")
        )
    
    def create(
        self,
        name: str,
        description: str,
        long_description: str = "",
        logo_url: str = "",
        is_public: bool = True
    ) -> Network:
        """
        Create a new network.
        
        Args:
            name: Network name
            description: Short description
            long_description: Long description (markdown)
            logo_url: Logo URL
            is_public: Whether network is public
            
        Returns:
            Created network
        """
        response = self._client.post("/v1/networks", {
            "name": name,
            "description": description,
            "longDescription": long_description,
            "logoUrl": logo_url,
            "isPublic": is_public
        })
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to create network"))
        
        data = response.get("data", {})
        
        return Network(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            long_description=data.get("longDescription", ""),
            logo_url=data.get("logoUrl", ""),
            status=data.get("status", "testing"),
            is_public=data.get("isPublic", True),
            users=data.get("users", 0),
            created_by=data.get("createdBy", ""),
            created_at=data.get("createdAt")
        )
    
    def get_members(self, network_id: str) -> List[MemberShort]:
        """
        Get network members.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of members
        """
        response = self._client.get(f"/v1/networks/{network_id}/members")
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to get members"))
        
        data = response.get("data", [])
        
        return [
            MemberShort(
                public_token=m["publicToken"],
                short_description=m.get("shortDescription", ""),
                role=m.get("role", "member")
            )
            for m in data
        ]

    def get_stats(self, network_id: str) -> dict:
        """
        Get network statistics.
        
        Args:
            network_id: Network ID
            
        Returns:
            Network stats including totalMembers, activeConversations, etc.
        """
        response = self._client.get(f"/v1/networks/{network_id}/stats")
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to get network stats"))
        
        return response.get("data", {})

    def discover(
        self,
        strategy: str = "popular",
        limit: int = 20
    ) -> dict:
        """
        Discover networks by strategy.
        
        Args:
            strategy: Strategy - 'popular', 'newest', 'unpopular', or 'recommended'
            limit: Maximum number of results
            
        Returns:
            Dictionary with networks, totalFound, and optional recommendedForYou
        """
        params = {
            "strategy": strategy,
            "limit": str(limit)
        }
        
        response = self._client.get("/v1/networks/discover", params=params)
        
        if not response.get("success"):
            raise APIError(response.get("error", {}).get("message", "Failed to discover networks"))
        
        return response.get("data", {})
