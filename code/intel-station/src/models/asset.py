from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UnlockedAsset:
    id: int | None = None
    user_id: int = 0
    asset_key: str = ""
    phase: int = 1
    substep: int = 1
    unlocked_at: datetime = field(default_factory=datetime.now)
