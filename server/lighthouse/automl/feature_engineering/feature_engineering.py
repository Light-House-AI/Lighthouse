import numpy as np
import pandas as pd
import json
from sklearn.feature_selection import chi2
from sklearn.utils import as_float_array, check_X_y, safe_sqr, safe_mask
from scipy import special

class FeatureEngineering:
    def __init__(self, data, cleaning_rules, target_column, problem_type):
        '''
        data: pandas dataframe
        cleaning_rules: json array of cleaning rules
        target_column: "column_name"
        problem_type: "Classification" or "Regression"
        '''
        self.data = data
        self.cleaning_rules = cleaning_rules
        self.target_column = target_column
        self.problem_type = problem_type
        self.rules = []
        
    def __remove_low_variance_features(self):
        self.data.drop(self.data.loc[:, self.data.var() < 0.01], axis = 1, inplace = True)
    
    def __remove_duplicate_features(self):
        self.data = self.data.T.drop_duplicates(keep='first').T
    
    def __remove_high_correlation_features(self):
        correlation_matrix = self.data.corr().abs()
        upper_tri = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape),k=1).astype(bool))
        to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
        self.data.drop(self.data[to_drop], axis = 1, inplace = True)
    
    def __remove_irrelevant_features(self):
        target = self.data[self.target_column]
        to_drop = []
        processed_features = [self.target_column]
        for column in self.cleaning_rules:
            if any(self.data.columns == column['column_name']):
                processed_features.append(column['column_name'])
                if column['is_numeric']:
                    if self.problem_type == 'Classification':
                        #ANOVA
                        F, P = f_classif(self.data[[column['column_name'],self.target_column]], target)
                        if P[0] > 0.05:
                            to_drop.append(column['column_name'])
                    else:
                        #Pearson
                        corr = self.data[column['column_name']].corr(target, method='pearson')
                        if abs(corr) < 0.05:
                            to_drop.append(column['column_name'])
                else:
                    if self.problem_type == 'Classification':
                        #Chi-Squared
                        F, P = chi2(self.data[[column['column_name'],self.target_column]], target)
                        if P[0] > 0.05:
                            to_drop.append(column['column_name'])
                    else:
                        #ANOVA
                        F, P = f_classif(self.data[[self.target_column,column['column_name']]], self.data[column['column_name']])
                        if P[0] > 0.05:
                            to_drop.append(column['column_name'])
        data_copy = self.data.copy()
        data_copy.drop(processed_features, axis = 1, inplace = True)
        for column in data_copy.columns:
            if self.problem_type == 'Classification':
                #Chi-Squared
                F, P = chi2(self.data[[column,self.target_column]], target)
                if P[0] > 0.05:
                    to_drop.append(column)
            else:
                #ANOVA
                F, P = f_classif(self.data[[self.target_column,column]], self.data[column])
                if P[0] > 0.05:
                    to_drop.append(column)
        self.data.drop(to_drop, axis = 1, inplace = True)

    def __get_strongly_correlated_features(self):
        corr_matrix = self.data.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        strongly_correlated = []
        for column in upper.columns:
            if column == self.target_column:
                continue
            for i, v in enumerate(upper[column]):
                if upper[column][i] > 0.75 and upper.iloc[i].name != self.target_column:
                    first_numeric = False
                    second_numeric = False
                    for object in self.cleaning_rules:
                        if object['column_name'] == column and object['is_numeric']:
                            first_numeric = True
                        elif object['column_name'] == upper.iloc[i].name and object['is_numeric']:
                            second_numeric = True
                    if first_numeric and second_numeric:    
                        strongly_correlated.append([column, upper.iloc[i].name])
        return strongly_correlated

    def __apply_PCA(self):
        strongly_correlated = self.__get_strongly_correlated_features()
        for X, Y in strongly_correlated:
            if X not in self.data.columns or Y not in self.data.columns:
                continue
            new_name = X + '_' + Y
            pca_input = self.data[[X,Y]]
            pca_input = featureNormalize(pca_input)
            U = pca(pca_input)
            Z = projectData(pca_input, U)
            Z = pd.DataFrame(Z)
            self.data.drop([X,Y], axis = 1, inplace = True)
            self.data[new_name] = Z
        
    def run(self):
        self.__remove_low_variance_features()
        self.__remove_duplicate_features()
        self.__remove_high_correlation_features()
        self.__remove_irrelevant_features()
        self.__apply_PCA()
        return self.data, self.rules

# PCA Funtions
def featureNormalize(X):
    mu = np.asarray(X).mean(axis=0)
    Y = np.asarray(X - mu)
    sigma = pow(np.var(Y, axis=0), 0.5)
    normalized_X = Y / sigma

    return normalized_X

def pca(X):
    cov = np.cov(X, rowvar=False)
    u, s, _ = np.linalg.svd(cov)
    return u

def projectData(X, U):
    Z = np.dot(np.asmatrix(X), np.asmatrix(U[:, :1]))
    return Z

# ANOVA Correlation
def f_oneway(*args):
    n_classes = len(args)
    args = [as_float_array(a) for a in args]
    n_samples_per_class = np.array([a.shape[0] for a in args])
    n_samples = np.sum(n_samples_per_class)
    ss_alldata = sum(safe_sqr(a).sum(axis=0) for a in args)
    sums_args = [np.asarray(a.sum(axis=0)) for a in args]
    square_of_sums_alldata = sum(sums_args) ** 2
    square_of_sums_args = [s ** 2 for s in sums_args]
    sstot = ss_alldata - square_of_sums_alldata / float(n_samples)
    ssbn = 0.
    for k, _ in enumerate(args):
        ssbn += square_of_sums_args[k] / n_samples_per_class[k]
    ssbn -= square_of_sums_alldata / float(n_samples)
    sswn = sstot - ssbn
    dfbn = n_classes - 1
    dfwn = n_samples - n_classes
    msb = ssbn / float(dfbn)
    msw = sswn / float(dfwn)
    f = msb / (msw + 1e-15)
    # flatten matrix to vector in sparse case
    f = np.asarray(f).ravel()
    prob = special.fdtrc(dfbn, dfwn, f)
    return f, prob


def f_classif(X, y):
    X, y = check_X_y(X, y, accept_sparse=['csr', 'csc', 'coo'])
    args = [X[safe_mask(X, y == k)] for k in np.unique(y)]
    return f_oneway(*args)