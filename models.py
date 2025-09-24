# models.py
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: str = ""          # "", "low", "med", "high"
    due: Optional[str] = None   # "YYYY-MM-DD"
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
