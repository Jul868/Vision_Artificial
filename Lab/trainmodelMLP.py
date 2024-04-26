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

workbook = xlrd.open_workbook('dataNumbers.xlsx') # Abrir libro de excel con los datos

# Función para cargar los datos del archivo de excek
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
        Xscaled, Y, test_size=0.3, random_state=42)

    # Configuración del modelo (red neuronal) 
    # MLPClassifier -> Clasificador de redes neuronales
    modelMLP = MLPClassifier(hidden_layer_sizes=(80, 60, 20, 15), # Tamaño de las capas ocultas (20 neuronas en dos capas ocultas)
                             max_iter=4000, # Iteraciones (épocas de entrenamiento)
                             activation='relu', # Función de activación
                             alpha=0.0001, # Parámetro para controlar la regularización 
                             learning_rate='adaptive', # Tasa de aprendizaje adaptativa
                             learning_rate_init=0.0001, # Tasa de aprendizaje inicial
                             batch_size=32, # Tamaño del lote 
                             beta_1=0.9, # Parámetro para el algoritmo de optimización
                             beta_2=0.999, # Parámetro para el algoritmo de optimización
                             epsilon=1e-08, # Parámetro para el algoritmo de optimización
                             random_state=42) # Semilla aleatoria para reproducibilidad


    
    # modelNDN.fit(X_train, Y_train)
    modelMLP.fit(X_train, Y_train) # Entrenamimento del modelo 

    # Evaluación del modelo 
    # accuracy = modelNDN.score(X_test, Y_test)
    accuracy = modelMLP.score(X_test, Y_test)
    accuracy = round(accuracy*100, 3)
    print(f"Accuracy: {accuracy} %")

    joblib.dump(modelScaler, 'modelScaler.joblib')
    # joblib.dump(modelNDN, 'modelNDN.joblib')
    joblib.dump(modelMLP, 'modelMLP.joblib') # Guardar el modelo entrenado 