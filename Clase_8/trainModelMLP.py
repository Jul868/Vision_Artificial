import numpy as np
import xlrd ## read excel file

##pip install xlrd==1.2.0
##pip install scikit-learn

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

import joblib

workbook = xlrd.open_workbook('dataNumbers.xlsx')


def load_workbook(file):
    sheet = file.sheet_by_index(0)
    x = np.zeros((sheet.nrows, sheet.ncols-1))
    y = []
    for i in range(0, sheet.nrows):
        for j in range(0, sheet.ncols-1):
            x[i, j] = sheet.cell_value(rowx=i, colx=j+1)
        y.append(sheet.cell_value(rowx=i, colx=0))
    y = np.array(y, np.float32)
    return x, y


if __name__ == '__main__':
    X, Y = load_workbook(workbook)
    modelScaler = StandardScaler()
    modelScaler.fit(X)
    Xscaled = modelScaler.transform(X)

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.15, random_state=42)

    modelMLP = MLPClassifier(hidden_layer_sizes=(
        80, 75, 60), max_iter=2000, activation='relu',learning_rate_init=0.001, alpha=0.0001, random_state=42,)#relu o logistic o tanh o identity o softmax
    modelMLP.fit(X_train, Y_train)

    # modelMLP = MLPClassifier(hidden_layer_sizes=(
    #     80, 65, 62), max_iter=2000, activation='tanh',learning_rate_init=0.0001, alpha=0.0001, random_state=42,)#relu o logistic o tanh o identity o softmax
    # modelMLP.fit(X_train, Y_train)

    #accuracy = modelNDN.score(X_test, Y_test)
    accuracy = modelMLP.score(X_test, Y_test)
    
    #Show accuracy in percentage with 3 decimals
    accuracy = round(accuracy*100, 3)
    print(f"Accuracy: {accuracy} %")

    joblib.dump(modelScaler, 'modelScaler.joblib')
    #joblib.dump(modelNDN, 'modelNDN3.joblib')
    joblib.dump(modelMLP, 'modelMLP_IFlat.joblib')