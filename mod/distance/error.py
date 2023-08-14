import numpy as np
from typing import List


def is_multivariate(data: List[np.ndarray]):
    return any(isinstance(data, np.ndarray) and len(data.shape) > 1 for data in data)
