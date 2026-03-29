from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union
from enum import Enum


class NetworkStatus(str, Enum):
    LIVE = "live"
    TESTING = "testing"


class MemberRole(str, Enum):
    MEMBER = "member"
    ADMIN = "admin"


class ConversationType(str, Enum):
    TOPIC = "topic"
    DIRECT = "direct"
    GROUP = "group"


class InvitationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class Network:
    id: Optional[str] = None
    name: str = ""
    description: str = ""
    long_description: str = ""
    logo_url: str = ""
    status: NetworkStatus = NetworkStatus.TESTING
    is_public: bool = True
    users: int = 0
    created_by: str = ""
    created_at: Optional[datetime] = None


@dataclass
class Member:
    id: Optional[str] = None
    network_id: str = ""
    public_token: str = ""
    short_description: str = ""
    long_description: str = ""
    role: MemberRole = MemberRole.MEMBER
    joined_at: Optional[datetime] = None


@dataclass
class Conversation:
    id: Optional[str] = None
    network_id: str = ""
    title: str = ""
    type: ConversationType = ConversationType.GROUP
    max_members: int = 10
    created_by: str = ""
    created_at: Optional[datetime] = None


@dataclass
class Message:
    id: Optional[str] = None
    conversation_id: str = ""
    sender_id: str = ""
    receiver_id: Optional[str] = None
    content: str = ""
    created_at: Optional[datetime] = None


@dataclass
class ProfileQuestion:
    id: Optional[str] = None
    network_id: str = ""
    question: str = ""
    order: int = 0
    required: bool = False


@dataclass
class KeyPair:
    public_token: str
    private_key: str


@dataclass
class AuthTokens:
    jwt: str
    expires_at: int
    public_token: str


@dataclass
class NetworkShort:
    id: str
    name: str
    description: str
    logo_url: str
    status: NetworkStatus
    users: int


@dataclass
class MemberShort:
    public_token: str
    short_description: str
    role: MemberRole
