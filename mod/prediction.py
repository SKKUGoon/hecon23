from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

import numpy as np

import time


def week_prediction(x: np.ndarray, y: np.ndarray, x_test: np.ndarray, tree: int=500, rf_state: int=42):
    """
    :@param x: includes 7일간의 과거 물품 품목 시계열 + 외생변수
    :@param y: 현재 물품 품목 시계열
    """

    # MCRF (Multivariate Count random forest)
    print("Creating model")
    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=tree,
            random_state=rf_state,
            criterion='poisson',  # because it's a count, use poisson
        )
    )
    print("Start fitting model")
    ts = time.time()
    model.fit(x, y)
    te = time.time()
    print(f"Fitting completed, {te-ts}s")

    predict_val = model.predict(x_test)
    print(predict_val)
    return predict_val
