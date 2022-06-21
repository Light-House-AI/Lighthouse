import pandas as pd
import numpy as np
from ray import method
from .data_cleaning import *


def get_columns_visualization(df, columns):
    """
    This function returns a dataframe with the columns selected by the user.
    """

    json_array = {}
    for col in columns:
        drop_missing_values(df, col)

        json = {}

        is_numeric, _ = is_numeric_or_categorical(df, col)
        json.update({"is_numeric": is_numeric})

        if is_numeric:
            json.update({'min': df[col].min(), 'max': df[col].max()})

        json_array.update({col: json})

    json_array.update({'data': df[columns].values.tolist()})

    return json_array


def get_correlation(df):
    return df.corr(method='pearson')
