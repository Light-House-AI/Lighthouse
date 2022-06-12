import pandas as pd
import numpy as np

import json
from typing import Dict, List
from .pipeline import clean_train, data_cleaning_suggestions


class NumpyEncoder(json.JSONEncoder):
    """ A custom JSON encoder that handles numpy data types. """
    def default(self, obj):
        if isinstance(obj, np.generic):
            return obj.item()
        else:
            return super(NumpyEncoder, self).default(obj)


def get_rows(file_path: str, skip: int = 0, limit: int = 100):
    """
    Returns rows from a file.
    """
    df = pd.read_csv(file_path, skiprows=range(1, skip + 1), nrows=limit)
    return df.to_json(orient='records')


def get_data_cleaning_suggestions(datasets_paths: List[str],
                                  predicted_column: str):
    """
    Returns data cleaning suggestions.
    """
    df = create_merged_data_frame(datasets_paths)
    rules = data_cleaning_suggestions(df, predicted_column)
    return json.dumps(rules, cls=NumpyEncoder)


def create_cleaned_dataset(raw_datasets_file_paths: List[str],
                           cleaned_dataset_file_path: str, rules: Dict,
                           predicted_column: str):
    """
    Returns cleaned dataset.
    """
    df = create_merged_data_frame(raw_datasets_file_paths)
    cleaned_df = clean_train(df, predicted_column, rules)
    cleaned_df.to_csv(cleaned_dataset_file_path, index=False)
    return True


def create_merged_data_frame(raw_datasets_file_paths: List[str]):
    """
    Returns merged data frame.
    """
    df = pd.concat((pd.read_csv(f) for f in raw_datasets_file_paths),
                   ignore_index=True)

    return df
