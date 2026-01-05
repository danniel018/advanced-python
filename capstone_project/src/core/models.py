from dataclasses import dataclass


# Domain models
@dataclass
class User:
    id: int | None
    username: str
    email: str
    age: int

@dataclass
class Message:
    id: int | None
    sender_id: int
    receiver_id: int
    content: str
