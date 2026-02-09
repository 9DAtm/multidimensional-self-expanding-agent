from dataclasses import dataclass, field
from typing import Dict
import time

@dataclass
class AwarenessState:
    field: Dict[str, float]
    coherence: float
    uncertainty: float
    timestamp: float = field(default_factory=time.time)