from __future__ import annotations
from enum import Enum

type Resample = Resample_ByCount | Resample_BySpacing | Resample_ByMaxSpacing

class DeviationMode(Enum):
    Absolute = 0
    Normal = 1
