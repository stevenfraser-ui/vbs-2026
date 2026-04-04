from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChatMessage:
    id: int | None = None
    user_id: int = 0
    role: str = ""  # "user" or "assistant"
    message: str = ""
    phase: int = 1
    stage: int = 1
    timestamp: datetime = field(default_factory=datetime.now)
