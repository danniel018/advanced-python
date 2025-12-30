from dataclasses import dataclass
from typing import Optional

# Domain models
@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    age: int

@dataclass
class Message:
    id: Optional[int]
    sender_id: int
    receiver_id: int
    content: str
