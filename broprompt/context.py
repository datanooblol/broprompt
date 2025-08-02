from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime, timezone

@dataclass
class Context:
    context: str
    metadata: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
