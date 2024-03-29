from .data_cleaning import *


def data_statistics(df, output_column):
    df_jsons = []
    for col in df.columns[df.columns != output_column]:
        drop_missing_values(df, col)

        col_json = {}
        col_json.update({"column_name": col})

        # Original datatype
        if df[col].dtype == 'object':
            col_json.update({"original_datatype": "object"})
        elif df[col].dtype == 'int64':
            col_json.update({"original_datatype": "int64"})
        elif df[col].dtype == 'float64':
            col_json.update({"original_datatype": "float64"})
        elif df[col].dtype == 'uint8':
            col_json.update({'original_datatype': 'uint8'})
        elif df[col].dtype == 'bool':
            col_json.update({'datatype': 'uint8'})

        # Correcting datatype
        detect_correct_datatype(df, col)

        # Detect Numeric or Categorical
        is_numeric = False
        if df[col].dtype != 'object':
            is_numeric, _ = is_numeric_or_categorical(df, col)

        col_json.update({'is_numeric': is_numeric})

        # Get Statistics (min, max, mean, mode, unique_count, unique_values)
        if is_numeric:
            col_json.update(
                {'min': df[col].min(), 'max': df[col].max(), 'mean': df[col].mean()})
            col_json.update(
                {'unique_count': None, 'unique_values': None, 'mode': None})
        elif df[col].dtype != 'object':
            col_json.update(
                {'min': df[col].min(), 'max': df[col].max(), 'mean': df[col].mean()})
            col_json.update({'unique_count': len(df[col].unique(
            )), 'unique_values': df[col].unique().tolist(), 'mode': float(df[col].mode()[0])})
        elif df[col].dtype == 'object':
            col_json.update({'min': None, 'max': None, 'mean': None})
            col_json.update({'unique_count': len(df[col].unique(
            )), 'unique_values': df[col].unique().tolist(), 'mode': df[col].mode()[0]})

        df_jsons.append(col_json)

    return df_jsons


def data_cleaning_suggestions(df, output_column):
    df_jsons = []
    for col in df.columns[df.columns != output_column]:
        col_json = {}
        col_json.update({"column_name": col})

        # Detect Datatype
        detect_correct_datatype(df, col)
        if df[col].dtype == 'object':
            col_json.update({"datatype": "object"})
        elif df[col].dtype == 'int64':
            col_json.update({"datatype": "int64"})
        elif df[col].dtype == 'float64':
            col_json.update({"datatype": "float64"})
        elif df[col].dtype == 'uint8':
            col_json.update({'datatype': 'uint8'})
        elif df[col].dtype == 'bool':
            col_json.update({'datatype': 'uint8'})

        # Detect Numeric or Categorical
        is_numeric = False
        if df[col].dtype != 'object':
            is_numeric, _ = is_numeric_or_categorical(df, col)
        col_json.update({'is_numeric': is_numeric})

        # Detect Outliers
        if is_numeric:
            outliers = detect_outliers_std(df, col)
            df = drop_rows_condition(df, outliers)
        elif df[col].dtype != 'object':
            outliers = detect_outliers_std(df, col)
            df = drop_rows_condition(df, outliers)
        elif df[col].dtype == 'object':
            df[col] = df[col].str.strip()
            df_temp = df.copy()
            convert_ordinal_category(
                df_temp, col, [x for x in range(len(df_temp[col].unique()))])
            outliers = detect_outliers_isolation_forest(df_temp, col, 0.05)
            try:
                df = correct_category_levenshtein(
                    df, col, df[outliers][col].unique())
            except:
                print(col, "ERROR: Levenshtein")
                df = drop_rows_condition(df, outliers)

        if is_numeric:
            col_json.update(
                {'min': df[col].min(), 'max': df[col].max(), 'mean': df[col].mean()})
            col_json.update(
                {'unique_count': len(df[col].unique()), 'unique_values': df[col].unique().tolist(), 'mode': float(df[col].mode()[0])})
        elif df[col].dtype != 'object':
            col_json.update(
                {'min': df[col].min(), 'max': df[col].max(), 'mean': df[col].mean()})
            col_json.update({'unique_count': len(df[col].unique(
            )), 'unique_values': df[col].unique().tolist(), 'mode': float(df[col].mode()[0])})
        elif df[col].dtype == 'object':
            col_json.update({'min': None, 'max': None, 'mean': None})
            col_json.update({'unique_count': len(df[col].unique(
            )), 'unique_values': df[col].unique().tolist(), 'mode': df[col].mode()[0]})

        # Missing Data Filler
        method, p_score = automatic_data_filler(
            df, col, output_column, is_numeric)
        col_json.update({'fill_method': method})
        col_json.update({'p_score': p_score})

        if method != 'column':
            col_json.update({'unique_count': len(
                df[col].unique()), 'unique_values': df[col].unique().tolist()})

        # completing json
        col_json.update({'is_nominal': True})
        col_json.update({'ordinal_order': []})

        df_jsons.append(col_json)

    return df_jsons


def clean_train(df, output_column, operations):
    for col_json in operations:
        # Column name
        col = col_json['column_name']

        # Check if column dropped
        if col_json['fill_method'] == 'column':
            remove_columns(df, [col])
            continue

        # Convert to datatype
        convert_to_datatype(df, col, col_json['datatype'])

        # Categorical or numeric
        is_numeric = col_json['is_numeric']

        # Detect Outliers
        if is_numeric:
            df = remove_outlier_numeric(
                df, col, col_json['min'], col_json['max'])
        elif df[col].dtype != 'object':
            df = remove_outlier_categorical(df, col, col_json['unique_values'])
        elif df[col].dtype == 'object':
            df[col] = df[col].str.strip()
            outliers = pd.array(
                list(set(df[col].unique().tolist()) - set(col_json['unique_values'])))                
            try:
                df = correct_category_levenshtein(df, col, outliers.to_numpy())
                df = drop_rows_condition(df, df[col].isin(outliers))
            except:
                df = drop_rows_condition(df, df[col].isin(outliers))

        # Fill missing data
        if col_json['fill_method'] == 'automatic':
            _ = automatic_data_filler(df, col, output_column, is_numeric)
        elif col_json['fill_method'] == 'average':
            fill_average_mode(df, col, is_numeric)
        elif col_json['fill_method'] == 'knn':
            knn_impute(df, col, is_numeric)
        elif col_json['fill_method'] == 'row':
            drop_missing_values(df, col)

        # Convert Nominal/Ordinal
        if not is_numeric:
            if col_json['is_nominal']:
                df = convert_nominal_categories(df, [col])
            else:
                convert_ordinal_category(df, col, col_json['ordinal_order'])

        # Normalizing data
        if is_numeric:
            normalize_column(df, col)

    return df


def clean_test(df, operations, raw_df, output_column):
    for col_json in operations:
        # Column name
        col = col_json['column_name']

        # Check if column dropped
        if col_json['fill_method'] == 'column':
            remove_columns(df, [col])
            continue

        # Convert to datatype
        convert_to_datatype(df, col, col_json['datatype'])

        # Categorical or numeric
        is_numeric = col_json['is_numeric']

        # Detect Outliers
        if is_numeric:
            outliers = detect_outlier_numeric(
                df, col, col_json['min'], col_json['max'])
            df.loc[outliers, col] = col_json['mean']

        elif df[col].dtype != 'object':
            outliers = detect_outlier_categorical(
                df, col, col_json['unique_values'])
            df.loc[outliers, col] = col_json['mode']

        elif df[col].dtype == 'object':
            df[col] = df[col].str.strip()
            outliers = [val for val in df[col].unique(
            ) if val not in col_json['unique_values']]
            try:
                df = correct_category_levenshtein(df, col, outliers)
                df[col].replace(to_replace=outliers, value=[col_json['mode']
                                for i in range(0, len(outliers))], inplace=True)
            except:
                df[col].replace(to_replace=outliers, value=[col_json['mode']
                                for i in range(0, len(outliers))], inplace=True)

        # Fill missing data
        if not is_numeric:
            df[col].fillna(col_json['mode'], inplace=True)
        else:
            df[col].fillna(col_json['mean'], inplace=True)

        # Convert Nominal/Ordinal
        if not is_numeric:
            if col_json['is_nominal']:
                df = convert_nominal_categories_test(
                    df, col, col_json['unique_values'])
            else:
                convert_ordinal_category_test(
                    df, col, col_json['unique_values'], col_json['ordinal_order'])

        # Normalizing data
        if is_numeric:
            normalize_column_test(df, col, raw_df)

    return df
