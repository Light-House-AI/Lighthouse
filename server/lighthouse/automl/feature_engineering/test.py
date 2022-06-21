import pandas as pd
import json
from feature_engineering import FeatureEngineering, apply_FE_rules

rules = json.load(open('../../../../notebooks/cars_rules.json'))
data = pd.read_csv('../../../../datasets/cleaned_datasets/cleaned_cars_01.csv')
data, feature_rules = FeatureEngineering(data, rules, 'price', 'Regression').run()
data.to_csv('cars_final.csv', index = False)

data_to_rules = pd.read_csv('../../../../datasets/cleaned_datasets/cleaned_cars_01.csv')
print(feature_rules)
apply_FE_rules(data_to_rules, feature_rules)

print(data.head())
print(data_to_rules.head())