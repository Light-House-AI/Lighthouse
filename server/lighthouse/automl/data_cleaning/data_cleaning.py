# LIBRARIES
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def read_data(file_name, header=0, sep=','):
    """
    Reads a csv file and returns a pandas dataframe
    """
    return pd.read_csv(file_name, sep=sep, header=header)


def try_parse_float(value):
    """
    Try to parse a string as a float
    """
    try:
        float(value)
    except:
        return False
    return True


def detect_correct_datatype(df, column):
    float_count = df[column].apply(
        lambda x: try_parse_float(x)).sum() - df[column].isna().sum()
    percentage_float = ((df.shape[0] - float_count) / df.shape[0]) * 100
    if percentage_float <= 25:
        df[column] = pd.to_numeric(df[column], errors='coerce')


def convert_type(val, type):
    """
    Convert a value to a given type
    """
    try:
        if type == 'int64':
            return np.int64(val)
        elif type == 'float64':
            return np.float64(val)
        elif type == 'uint8':
            return np.uint8(val)
    except:
        return None


def is_numeric_or_categorical(df, column):
    unique_values = df[column].unique()
    if ((df.shape[0] - len(unique_values)) / df.shape[0]) * 100 < 93:
        return True, ((df.shape[0] - len(unique_values)) / df.shape[0]) * 100
    return False, ((df.shape[0] - len(unique_values)) / df.shape[0]) * 100


def remove_columns(df, columns):
    """
    Removes columns from a dataframe
    """
    df.drop(columns, axis=1, inplace=True)


def remove_rows(df, rows):
    """
    Removes rows from a dataframe
    """
    df.drop(rows, axis=0, inplace=True)


def drop_rows_condition(df, conition):
    return df[~conition]


def remove_duplicates(df):
    """
    Removes duplicates from a dataframe
    """
    df.drop_duplicates(inplace=True)


def convert_to_datatype(df, column, datatype):
    """
    Converts a column to a datatype
    """
    if datatype == 'object':
        df[column] = df[column].astype(datatype)
    else:
        df[column] = df[column].apply(lambda x: convert_type(x, datatype))

    return df


def remove_outlier_numeric(df, column, min=-np.inf, max=np.inf):
    """
    Removes rows from a dataframe based on a condition
    """
    if min != -np.inf and max != np.inf:
        return df[((df[column] >= min) & (df[column] <= max)) | df[column].isna()]
    elif min == -np.inf and max != np.inf:
        return df[(df[column] <= max) | df[column].isna()]
    elif min != -np.inf and max == np.inf:
        return df[(df[column] >= min) | df[column].isna()]


def detect_outlier_numeric(df, column, min=-np.inf, max=np.inf):
    """
    Removes rows from a dataframe based on a condition
    """
    if min != -np.inf and max != np.inf:
        return ~((df[column] >= min) & (df[column] <= max))
    elif min == -np.inf and max != np.inf:
        return ~(df[column] <= max)
    elif min != -np.inf and max == np.inf:
        return ~(df[column] >= min)


def remove_outlier_categorical(df, column, unique_values):
    """
    Removes rows from a dataframe based on a condition
    """
    inconsistent_categories = pd.array(
        list(set(df[column].unique()) - set(unique_values)))
    return df[(~df[column].isin(inconsistent_categories)) | df[column].isna()]


def detect_outlier_categorical(df, column, unique_values):
    """
    Removes rows from a dataframe based on a condition
    """
    inconsistent_categories = pd.array(
        list(set(df[column].unique()) - set(unique_values)))
    return df[column].isin(inconsistent_categories)


def detect_outliers_std(df, column, std=3):
    """
    Detect outliers based on standard deviation
    """

    # Set upper and lower limit to 3 standard deviation
    random_data_std = np.std(df[column])
    random_data_mean = np.mean(df[column])
    anomaly_cut_off = random_data_std * std

    lower_limit = random_data_mean - anomaly_cut_off
    upper_limit = random_data_mean + anomaly_cut_off

    # Generate outliers
    outliers = (df[column] < lower_limit) | (df[column] > upper_limit)
    return outliers


def detect_outliers_isolation_forest(df, column, contamination=0.1):
    """
    Detect outliers based on isolation forest
    """
    # Create isolation forest
    clf = IsolationForest(random_state=0, contamination=contamination)
    predictions = clf.fit_predict(df[column].to_numpy().reshape(-1, 1))
    return predictions == -1


def correct_category_levenshtein(df, column, incorrect_categories, threshold=80):
    """
    Corrects a column by using fuzzywuzzy to find the correct category
    """
    # inconsistent_categories = pd.array(list(set(df[column].unique()) - set(incorrect_categories)))
    inconsistent_categories = pd.array(list(incorrect_categories))
    inconsistent_categories = inconsistent_categories[~inconsistent_categories.isna(
    )]

    correct_categories = pd.array(
        list(set(df[column].unique()) - set(incorrect_categories)))

    for inconsistent_category in inconsistent_categories:
        if not pd.isna(inconsistent_category):
            potential_match = process.extractOne(
                inconsistent_category, correct_categories)
            if potential_match[1] > threshold:
                df.loc[df[column] == inconsistent_category,
                       column] = potential_match[0]
    return df


def convert_nominal_categories(df, columns):
    """
    Converts categorical data to numeric data
    """
    return pd.get_dummies(df, columns=columns)


def convert_nominal_categories_test(df, column, unique_values):
    column_names_unique = []
    for unique in unique_values:
        column_names_unique.append(column + '_' + str(unique))

    df[column_names_unique] = 0
    for unique in df[column].unique():
        df[column + '_' + str(unique)] = 1

    remove_columns(df, [column])
    return df


def convert_ordinal_category(df, column, order):
    df[column].replace(to_replace=df[column].unique(),
                       value=order, inplace=True)


def fill_missing_values(df, column, value):
    """
    Fills missing values in a column with a value
    """
    df[column].fillna(value, inplace=True)


def drop_missing_values(df, column):
    """
    Drops missing values in a column
    """
    df.dropna(subset=[column], inplace=True)


def fill_average_mode(df, column, is_numeric):
    """
    Fills missing values in a column with the average or mode
    """
    if not is_numeric:
        df[column].fillna(df[column].mode()[0], inplace=True)
    else:
        df[column].fillna(df[column].mean(), inplace=True)


def knn_impute(df, column, is_numeric):
    """
    Imputation using KNN
    """
    x_train = df[~df[column].isna()].copy()
    x_train.dropna(inplace=True)

    y_train = x_train[column]
    x_train = x_train[x_train.columns[x_train.columns != column]]
    x_train = x_train[x_train.columns[x_train.dtypes != 'object']]

    x_predict = df[df[column].isna()][df.columns[df.columns != column]].copy()
    x_predict = x_predict[x_predict.columns[x_predict.dtypes != 'object']]

    if x_predict.shape[0] == 0:
        return

    if is_numeric:
        # REGRESSION
        knn_regressor = KNeighborsRegressor()
        knn_regressor.fit(x_train, y_train)
        y_predict = knn_regressor.predict(x_predict)
        df.loc[df[column].isna(), column] = y_predict
    else:
        # CLASSIFICATION
        knn_classifier = KNeighborsClassifier()
        knn_classifier.fit(x_train, y_train)
        y_predict = knn_classifier.predict(x_predict)
        df.loc[df[column].isna(), column] = y_predict


def knn_impute_test(raw_df, column, is_numeric, shadow_df, output_column, shadow_clone_df):
    x_predict = shadow_clone_df[shadow_clone_df.columns[shadow_clone_df.columns != column]].copy(
    )
    x_predict = x_predict[x_predict.columns[x_predict.dtypes != 'object']]

    x_train = raw_df.copy()

    y_train = x_train[column]
    x_train = x_train[x_predict.columns]
    x_train = x_train[x_train.columns[x_train.dtypes != 'object']]

    if x_predict.shape[0] == 0:
        return

    if is_numeric:
        # REGRESSION
        knn_regressor = KNeighborsRegressor()
        knn_regressor.fit(x_train, y_train)
        y_predict = knn_regressor.predict(x_predict)
        shadow_df.loc[shadow_df[column].isna(), column] = y_predict
    else:
        # CLASSIFICATION
        knn_classifier = KNeighborsClassifier()
        knn_classifier.fit(x_train, y_train)
        y_predict = knn_classifier.predict(x_predict)
        shadow_df.loc[shadow_df[column].isna(), column] = y_predict


def pearson_score(df, column, output_column):
    df_temp = df.copy()
    drop_missing_values(df_temp, column)
    if df_temp[column].dtype == 'object':
        convert_ordinal_category(
            df_temp, column, [x for x in range(len(df_temp[column].unique()))])

    p_score = df_temp[column].corr(df_temp[output_column], method='pearson')
    return p_score


def automatic_data_filler(df, column, output_column, is_numeric, no_corr=0.01, low_corr=0.5):

    p_score = pearson_score(df, column, output_column)

    if df[column].isna().sum() == 0:
        # print(column, ': No missing values')
        return 'automatic', p_score

    if p_score >= -no_corr and p_score <= no_corr:
        # NO CORRELATION
        if ((df.shape[0] - df[column].isna().sum()) / df.shape[0]) * 100 >= 50:
            # MISSING VALUES ARE TOO LARGE
            # print(column, p_score, "No correlation, missing values too large")
            remove_columns(df, [column])
            return 'column', p_score
        else:
            # MISSING VALUES ARE SMALL
            # print(column, p_score, "No correlation, missing values small")
            drop_missing_values(df, column)
            return 'row', p_score
    elif (p_score >= -low_corr and p_score < -no_corr) or (p_score > no_corr and p_score <= low_corr):
        # LOW CORRELATION
        # print(column, p_score, "Low correlation")
        fill_average_mode(df, column, is_numeric)
        return 'average', p_score
    elif p_score >= -1 and p_score <= 1:
        # HIGH CORRELATION
        # print(column, p_score, "High correlation")
        knn_impute(df, column, is_numeric)
        return 'knn', p_score


def normalize_column(df, column):
    df[column] = StandardScaler().fit_transform(
        df[column].values.reshape(-1, 1))


def normalize_column_test(df, column, raw_df):
    scaler = StandardScaler()
    scaler.fit_transform(raw_df[column].values.reshape(-1, 1))
    df[column] = scaler.transform(df[column].values.reshape(-1, 1))
