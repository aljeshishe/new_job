"""A sample module."""
from collections import deque
from itertools import tee
from typing import Dict, Any, Callable

import log
import numpy as np


def normalize(d: Dict[str, Any], exceptions: list[Callable[[str, Any], bool]]) -> Dict[str, Any]:
    result = {}

    def _normalize(d, keys=deque()):
        for k, v in d.items():
            if any(exception(k, v) for exception in exceptions):
                continue
            if isinstance(v, dict):
                _normalize(d=v, keys=keys + deque([k]))
                continue
            keys_str = "_".join(keys + deque([k]))
            result[keys_str] = v
        return result

    return _normalize(d=d)

def gen_ranges(start, end, steps):
    g1, g2 = tee(np.linspace(start, end, steps + 1, endpoint=True))
    next(g2)
    for start, end in zip(g1, g2):
        yield start, end

