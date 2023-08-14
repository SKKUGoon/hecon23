# Paparrizos J and Gravano L (2015). ``k-Shape: Efficient and Accurate Clustering of Time Series.''
# In *Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data*, series
# SIGMOD '15, pp. 1855-1870. ISBN 978-1-4503-2758-9, \doi{10.1145/2723372.2737793}.

import numpy as np


def cross_correlation_coefficent():
    ...


def distance():
    # Cross-correlation based distance (CCBD)
    # Use absolute value of Shape Based Distance (SBD)
    ...


def ncc_calculation(x: np.ndarray, y: np.ndarray, debug: bool = False):
    """
    Uses the FFT to compute the cross-correlation sequence between 2 series.
        2 sequences can have different length
    :param x:
    :param y:
    :param debug:
    :return:
    """
    if debug:
        print("NCC calculation with FFT")

    
    ...
