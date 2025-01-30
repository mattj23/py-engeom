from __future__ import annotations

from pathlib import Path
from typing import Any, List, Tuple, Union
from enum import Enum

import numpy


class DeviationMode(Enum):
    Absolute = 0
    Normal = 1


