from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

import numpy as np


def week_prediction(data: np.ndarray, tree: int, rf_state: int):
    # MCRF (Multivariate Count random forest)
    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=tree,
            random_state=rf_state,
            criterion='poisson',  # because it's a count, use poisson
        )
    )

    model.fit(..., ...)
    y_hat = model.predict(...)

    ...




