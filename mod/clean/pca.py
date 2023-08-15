# Use PCA (Principal Component Analysis) to
# reduce the dimension of the working data

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from typing import List, Dict


def check_series_num(data: pd.DataFrame) -> int:
    """
    :param data: Dataframe with reset index
    :return: Number of time series in a given dataframe without the index column
    """
    return len(data.columns)


def prep_pca(data_ls: List[pd.DataFrame], time_frame: int) -> pd.DataFrame:
    whole = pd.concat(data_ls, axis=1)
    return whole[:time_frame]


def reduce_dim(data_ls: List[pd.DataFrame],
               n_components: int = 19,
               standardize: bool = True,
               time_frame: int = None,
               debug: bool = False) -> Dict:
    """
    Concatenate all the dataframe in the `data_ls` by `concat_key`.
    Reduce the column space dimension using PCA.

    It is asserted in the power-point presentation that
    19 principal component accounts for up to 75% explanation power.

    :return: DataFrame with reduced dimension.
    """
    if time_frame is None:
        # Use 215 data points (page 6)
        time_frame = 215

    data = prep_pca(data_ls, time_frame)
    data_dates = data.index

    # Step 1: Standarize the data
    scaler = None
    if standardize:
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

    # Step 2: Apply PCA
    pca = PCA(n_components=n_components)
    x_pca = pca.fit_transform(data)

    # Convert the PCA result into a DataFrame
    df_pca = pd.DataFrame(
        x_pca,
        columns=[f"PC{i+1}" for i in range(x_pca.shape[1])],
    )
    df_pca.index = data_dates  # Apply original index(dates)

    if debug:
        print("PCA successful")
        print(df_pca.head(3))

    return {
        # Processing model class
        "pca_model": pca,
        "scaler": scaler if standardize else None,

        # Processed data
        "pc": df_pca,

        # Statistics
        "explained_var": explained_var(pca, debug=debug),
    }


def explained_var(model: PCA, debug: bool):
    exp_var = model.explained_variance_ratio_
    if debug:
        print(f"Explained Variance by each component: {exp_var}")
        print(f"Total Explained Variance(for the selected components): {np.sum(exp_var)}")
    return exp_var

