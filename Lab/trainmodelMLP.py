import numpy as np
import xlrd ## Libreria para leer archivos de excel 

## pip install xlrd==1.2.0
## pip install scikit-learn

from sklearn.neural_network import MLPClassifier # Clasificador de redes neuroanles
from sklearn.preprocessing import StandardScaler # Escalador de características 
from sklearn.model_selection import train_test_split # Función para dividir datos en conjuntos de entranmiento y prueba 
from sklearn.metrics import accuracy_score, confusion_matrix # Métricas de evaluación del modelo 
from sklearn.neighbors import KNeighborsClassifier # Clasificador de vecinos más cercanos

import joblib # Herramienta para guardar y cargar modelos entrenados 

workbook = xlrd.open_workbook('dataDientes.xlsx') # Abrir libro de excel con los datos

# Función para cargar los datos del archivo de excel
def load_workbook(file):
    sheet = file.sheet_by_index(0)
    x = np.zeros((sheet.nrows, sheet.ncols-1)) # sheet.nols-1 -> le quito la columna de la clase
    y = [] # Vector para guardar los datos 
    for i in range(0, sheet.nrows):
        for j in range(0, sheet.ncols-1):
            x[i, j] = sheet.cell_value(rowx=i, colx=j+1) # colx=j+1 -> los datos empiezan en la segunda columna (la primera es la clase)
        y.append(sheet.cell_value(rowx=i, colx=0))
    y = np.array(y, np.float32)
    return x, y


if __name__ == '__main__':
    X, Y = load_workbook(workbook) # Cargar datos con la función

    # Escalado de características -> Obtener una media de 0 y una desviación estándar de 1
    modelScaler = StandardScaler()
    modelScaler.fit(X)
    Xscaled = modelScaler.transform(X)

    # División de datos en conjunto de entrenamiento y prueba  
    X_train, X_test, Y_train, Y_test = train_test_split(
        Xscaled, Y, test_size=0.15, random_state=42)

    # Configuración del modelo (red neuronal) 
    # MLPClassifier -> Clasificador de redes neuronales
    modelMLP = MLPClassifier(hidden_layer_sizes=(70, 100), max_iter=4000, activation='logistic',learning_rate_init=0.001, alpha=0.001, random_state=42)
    # Entrenamiento del modelo
    modelMLP.fit(X_train, Y_train) 

    # Evaluación del modelo 
    accuracy = modelMLP.score(X_test, Y_test)
    accuracy = accuracy * 100
    print('accuracy: ', accuracy)

    #joblib.dump(modelScaler, 'modelScaler.joblib')
    #joblib.dump(modelMLP, 'modelMLP.joblib') # Guardar el modelo entrenado
    
    #modelo flatten
    joblib.dump(modelMLP, 'ModelF.joblib') # Guardar el modelo entrenado
    joblib.dump(modelScaler, 'modelScalerF.joblib') # Guardar el modelo entrenado