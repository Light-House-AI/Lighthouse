import numpy as np

from sklearn.preprocessing import StandardScaler, normalize
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_auc_score

from model_creator.neural_network.network_generator import NetworkGenerator, to_categorical

X, Y = load_wine(return_X_y=True)
print(X.shape, Y.shape)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2)
#Normalizing data
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

network = NetworkGenerator(X_train, y_train, X_test, y_test, "Classification").import_model("wine_classification.pkl")

y_pred = np.array(network.predict(X_test))
print(accuracy_score(y_test, y_pred.round()))