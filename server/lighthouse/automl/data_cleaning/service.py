import pandas as pd
import numpy as np

import json
from typing import Dict, List

from .pipeline import (
    clean_test,
    clean_train,
    data_cleaning_suggestions,
    data_statistics,
)


class NumpyEncoder(json.JSONEncoder):
    """ A custom JSON encoder that handles numpy data types. """
    def default(self, obj):
        if isinstance(obj, np.generic):
            return obj.item()
        else:
            return super(NumpyEncoder, self).default(obj)


def get_cleaned_input_data(input_data: Dict, raw_dataset_path: str,
                           predicted_column: str, rules: List[Dict]):
    """
    Returns cleaned input data.
    """
    input_data_df = pd.DataFrame([input_data])
    raw_data = pd.read_csv(raw_dataset_path)
    return clean_test(input_data_df, rules, raw_data, predicted_column)


def get_rows(file_path: str, skip: int = 0, limit: int = 100):
    """
    Returns rows from a file.
    """
    df = pd.read_csv(file_path, skiprows=range(1, skip + 1), nrows=limit)
    return df.to_json(orient='records')


def get_dataset_statistics(dataframe: pd.DataFrame, predicted_column: str):
    """
    Returns dataset statistics.
    """
    stats = data_statistics(dataframe, predicted_column)
    return json.dumps(stats, cls=NumpyEncoder)


def get_data_cleaning_suggestions(dataframe: pd.DataFrame,
                                  predicted_column: str):
    """
    Returns data cleaning suggestions.
    """
    rules = data_cleaning_suggestions(dataframe, predicted_column)
    return json.dumps(rules, cls=NumpyEncoder)


def create_save_cleaned_dataset(raw_dataset_dataframe: pd.DataFrame,
                                cleaned_dataset_file_path: str, rules: Dict,
                                predicted_column: str):
    """
    Creates and save a cleaned dataset.
    Returns cleaned dataset.
    """
    cleaned_df = clean_train(raw_dataset_dataframe, predicted_column, rules)
    cleaned_df.to_csv(cleaned_dataset_file_path, index=False)
    return cleaned_df


def create_save_merged_dataframe(datasets_paths: List[str], file_path: str):
    """
    Creates and save a merged data frame.
    Returns the merged data frame.
    """
    df = create_merged_data_frame(datasets_paths)
    df.to_csv(file_path, index=False)
    return df


def create_merged_data_frame(datasets_paths: List[str]):
    """
    Returns merged data frame.
    """
    df = pd.concat((pd.read_csv(f) for f in datasets_paths), ignore_index=True)
    return df


def save_dataframe(dataframe: pd.DataFrame, file_path: str):
    """
    Saves a dataframe.
    """
    dataframe.to_csv(file_path, index=False)


def get_dataset_columns(file_path: str):
    """
    Returns dataset columns.
    """
    df = pd.read_csv(file_path)
    return df.columns.to_list()