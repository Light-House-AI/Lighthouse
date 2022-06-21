import pandas as pd
import json
from feature_engineering import FeatureEngineering

rules = json.load(open('../data_cleaning/suggestions.json'))
data = pd.read_csv('../../../../datasets/supermarket/cleaned_data.csv')
data, feature_rules = FeatureEngineering(data, rules, 'Sales', 'Regression').run()
data.to_csv('supermarket_final.csv', index = False)