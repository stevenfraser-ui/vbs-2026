from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int | None = None
    name: str = ""
    code: str = ""
    age: int = 0
    current_phase: int = 1
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
