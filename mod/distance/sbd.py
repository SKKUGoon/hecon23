# Transcripting "https://github.com/asardaes/dtwclust/blob/master/R/DISTANCES-sbd.R"
# Function `sbd_proxy` uses C++ Code. Because of time issue - won't use it now.

import numpy as np
from scipy.stats import zscore

from .ncc import ncc_calculation
from .error import is_multivariate


def shape_based_distance(x: list | np.ndarray,
                         y: list | np.ndarray,
                         z_norm: bool = False,
                         shifted: bool = True,
                         project_override: bool = False):
    # Check data type and shape
    if is_multivariate([np.array(x), np.array(y)]):
        print("sbd error: not supported")

    # Make sure that array x has the lesser length
    if len(x) > len(y):
        x, y = y, x

    if z_norm:
        # Return Z-score of a sequence (normalization process)
        # If `project_override` is True, return with absolute value on numerator
        cross_corr_sequence = ncc_calculation(zscore(x), zscore(y), project_override=project_override)
    else:
        cross_corr_sequence = ncc_calculation(x, y, project_override=project_override)

    m = np.max(cross_corr_sequence)

    if not shifted:
        return {"dist": 1 - m, "yshift": None}

    # Returns the index of the maximum value in the `cross_corr_sequcne`
    # = Identifies the position in the cross_correlation sequcne that has the highest correlation between `x` and `y`
    shift = np.argmax(cross_corr_sequence) - max(len(x), len(y))

    if shift < 0:
        yshift = y[-shift : len(y)]
    else:
        yshift = np.concatenate((np.zeros(shift), y))

    if len(yshift) < len(x):
        yshift = np.concatenate((yshift, np.zeros(len(x) - len(yshift))))
    else:
        yshift = yshift[:len(x)]

    return {"dist": 1 - m, "yshift": yshift}


