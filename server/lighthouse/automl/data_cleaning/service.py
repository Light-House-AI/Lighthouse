import pandas as pd

from typing import Dict, List
from .pipeline import clean_train, data_cleaning_suggestions


def get_rows(file_path: str, skip: int = 0, limit: int = 100):
    """
    Returns rows from a file.
    """
    df = pd.read_csv(file_path, skiprows=range(1, skip + 1), nrows=limit)
    return df.to_json(orient='records')


def get_data_cleaning_suggestions(file_path: str, predicted_column: str):
    """
    Returns data cleaning suggestions.
    """
    df = pd.read_csv(file_path)
    return data_cleaning_suggestions(df, predicted_column)


def create_cleaned_dataset(raw_datasets_file_paths: List[str],
                           cleaned_dataset_file_path: str, rules: Dict,
                           predicted_column: str):
    """
    Returns cleaned dataset.
    """
    df = pd.concat((pd.read_csv(f) for f in raw_datasets_file_paths),
                   ignore_index=True)

    cleaned_df = clean_train(df, predicted_column, rules)
    cleaned_df.to_csv(cleaned_dataset_file_path, index=False)
    return True