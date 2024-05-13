import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import cross_val_score

x, y = datasets.load_iris(return_X_y=True) # Cargamos el dataset de iris en x, y 
x.shape, y.shape # Verificamos las dimensiones de x, y

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0) # Dividimos el dataset en entrenamiento(60%) y prueba (40%)

x_train.shape, y_train.shape, x_test.shape, y_test.shape # Verificamos las dimensiones de x_train, y_train, x_test, y_test


clf = svm.SVC(kernel='linear', C=100, random_state=42)
scores = cross_val_score(clf, x_train, y_train, cv=5) # Evaluamos el clasificador con validación cruzada
 # cv es el número de pliegues, a mayor número de pliegues, mayor tiempo de ejecución y mejor evaluación del clasificador

#accuracy = clf.score(x_test, y_test) # Evaluamos el clasificador con el conjunto de prueba

#print(accuracy)
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std())) # Imprimimos la precisión del clasificador

#si el promedio (scores.mean()) es mayor a 95% se guarla el modelo de clf con el fit 
if scores.mean() > 0.95:
    clf = svm.SVC(kernel='linear', C=1).fit(x_train, y_train) # Creamos un clasificador de máquinas de soporte vectorial 
    #svm es un clasificador genera una linea que separa los datos en dos clases
    #print("Modelo guardado")
    #np.save('model.npy', clf) # Guardamos el modelo en un archivo .npy