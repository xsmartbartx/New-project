from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class GrooveTemplate:
    name: str
    description: str
    swing_percent: float


BUILT_IN_GROOVES: Dict[str, GrooveTemplate] = {
    "straight": GrooveTemplate(name="straight", description="No swing, grid-tight.", swing_percent=0.0),
    "mpc_light": GrooveTemplate(name="mpc_light", description="Light MPC-style swing.", swing_percent=12.0),
    "mpc_medium": GrooveTemplate(name="mpc_medium", description="Medium MPC-style swing.", swing_percent=18.0),
    "mpc_heavy": GrooveTemplate(name="mpc_heavy", description="Heavy MPC-style swing.", swing_percent=26.0),
}


def get_groove(name: str) -> Optional[GrooveTemplate]:
    return BUILT_IN_GROOVES.get(name)

