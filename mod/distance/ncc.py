# Paparrizos J and Gravano L (2015). ``k-Shape: Efficient and Accurate Clustering of Time Series.''
# In *Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data*, series
# SIGMOD '15, pp. 1855-1870. ISBN 978-1-4503-2758-9, \doi{10.1145/2723372.2737793}.

import numpy as np

from mod.distance.error import is_multivariate


def l2norm(array: np.ndarray) -> float:
    """
     Calculate the L2 norm (Euclidean norm) of an array
    """
    return np.linalg.norm(array)


def ncc_calculation(x: list | np.ndarray,
                    y: list | np.ndarray,
                    debug: bool = False,
                    project_override: bool = False):
    """
    Uses the FFT to compute the cross-correlation sequence between 2 series.
        2 sequences can have different length
    :param x: Univariate time series
    :param y: Univariate time series
    :param debug:
    :return: The cross-correlation sequence with length `length(x) + length(y) - 1L`.
    """
    if is_multivariate([np.array(x), np.array(y)]):
        print("sbd error: not supported")

    # Match type
    xflt = np.array(x, dtype=float)
    yflt = np.array(y, dtype=float)

    den = l2norm(xflt) * l2norm(yflt)
    if den == 0:
        if debug:
            print(f"l2norm was 0 (x = {l2norm(xflt)}, y = {l2norm(yflt)}). Returning inf")
        return float('inf')
    else:
        # mode='valid'.
        # Return the convolution that is the size of the larger input.
        # np.conj. Used to obtain the complex conjugate of an array.
        #   If x, and y are real numbers, this conjugate has no effect.
        convolution_result = np.convolve(x, np.conj(y), mode='full')
        if project_override:
            if debug:
                print("Printing project_overrided result. Put absolute value to the numerator")
            return np.abs(convolution_result) / den
        else:
            return convolution_result / den


def test_ncc():
    x = [-1, -2, 3, 4]
    y = [1, 2, 3, 4]

    test_result = ncc_calculation(x, y, project_override=True)
    print(test_result)
    print(test_result.shape)


if __name__ == "__main__":
    test_ncc()
