import numpy as np

# https://scikit-learn.org/stable/auto_examples/ensemble/plot_random_forest_regression_multioutput.html#sphx-glr-auto-examples-ensemble-plot-random-forest-regression-multioutput-py


def sigmoid(x):
    return 1 / (1 + np.exp(-1 * x))


def weighted_bonferroni():
    # Z-normalize the price * -1 Sigmoid 함수에 적용
    
    ...