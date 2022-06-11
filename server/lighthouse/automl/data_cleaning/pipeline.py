from server.lighthouse.automl.data_cleaning.data_cleaning import *


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

        # Missing Data Filler
        method, p_score = automatic_data_filler(
            df, col, output_column, is_numeric)
        col_json.update({'fill_method': method})
        col_json.update({'p_score': p_score})

        if method != 'column' and not is_numeric:
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
                list(set(df[col].unique()) - set(col_json['unique_values'])))
            try:
                df = correct_category_levenshtein(df, col, outliers.to_numpy())
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
        if df[col].dtype == 'object':
            if col_json['is_nominal']:
                df = convert_nominal_categories(df, [col])
            else:
                convert_ordinal_category(df, col, col_json['ordinal_order'])

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
            df[col][outliers] = col_json['mean']
        elif df[col].dtype != 'object':
            outliers = detect_outlier_categorical(
                df, col, col_json['unique_values'])
            df[col][outliers] = col_json['mode']
        elif df[col].dtype == 'object':
            df[col] = df[col].str.strip()
            outliers = pd.array(
                list(set(df[col].unique()) - set(col_json['unique_values'])))
            try:
                df = correct_category_levenshtein(df, col, outliers.to_numpy())
            except:
                df[col][outliers] = col_json['mode']

        # Fill missing data
        if col_json['fill_method'] == 'automatic' or col_json['fill_method'] == 'row':

            p_score = col_json['p_score']
            if p_score >= -0.5 and p_score <= 0.5:
                if not is_numeric:
                    df[col].fillna(col_json['mode'], inplace=True)
                else:
                    df[col].fillna(col_json['mean'], inplace=True)
            else:
                knn_impute_test(raw_df, col, is_numeric, df, output_column)

        elif col_json['fill_method'] == 'average':
            fill_average_mode(df, col, is_numeric)
        elif col_json['fill_method'] == 'knn':
            knn_impute_test(raw_df, col, is_numeric, df, output_column)

        # Convert Nominal/Ordinal
        if df[col].dtype == 'object':
            if col_json['is_nominal']:
                df = convert_nominal_categories(df, [col])
            else:
                convert_ordinal_category(df, col, col_json['ordinal_order'])

    return df
