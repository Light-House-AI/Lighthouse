import pandas as pd
import numpy as np
from ray import method
from data_cleaning import *


def get_columns_visualization(df, columns):
    """
    This function returns a dataframe with the columns selected by the user.
    """
    drop_missing_values(df, columns)
    json_array = []
    for col in columns:
        json = {}
        json.update({"column_name": col})

        is_numeric, _ = is_numeric_or_categorical(df, col)
        json.update({"is_numeric": is_numeric})
        
        if is_numeric:
            json.update({'min': df[col].min(), 'max': df[col].max()})

        json_array.append(json)
        
    json_array.append({'data': df[columns]})
    
    return json_array

def get_correlation(df):
    return df.corr(method='pearson')
