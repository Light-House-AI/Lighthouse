import pandas as pd
import json
from feature_engineering import FeatureEngineering

rules = json.load(open('cars_rules.json'))
data = pd.read_csv('cleaned_cars.csv')
data, feature_rules = FeatureEngineering(data, rules, 'price', 'Regression').run()
data.to_csv('cars_final.csv', index = False)