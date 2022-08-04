#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 20:10:37 2022

@author: spatricio
"""

import pandas as pd

from sklearn.manifold import MDS
from matplotlib import pyplot as plt

import seaborn as sns         

from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
from sklearn import datasets
from scipy.cluster.hierarchy import ClusterWarning
import warnings
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import numpy as np
import random
from random import sample
from sklearn.model_selection import KFold
from sklearn.model_selection import LeaveOneOut

warnings.filterwarnings("ignore")


iris = datasets.load_iris()
iris_df=pd.DataFrame(iris.data)
iris_df['Species']=iris.target
iris_df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'Species']
iris_df.dropna(how="all", inplace=True) # remove any empty lines
iris_X=iris_df.iloc[:,[0,1,2,3,4]]


iris_X["Species"]= ["Iris-setosa" if value==0 else value for value in list(iris_X["Species"])]
iris_X["Species"]= ["Iris-versicolor" if value==1 else value for value in list(iris_X["Species"])]
iris_X["Species"]= ["Iris-virginica" if value==2 else value for value in list(iris_X["Species"])]


iris_es = iris_X["Species"]
iris_df["Species"] =iris_X["Species"]
dataset=iris_df.iloc[:,[0,1,2,3,4]]
cant_datos = 100
train = 0.51
test = 1-train
dataset = dataset[0:cant_datos]
#print(dataset)


###########################Random Cross-Validation######################################
#d2 = dataset.sample(cant_datos,random_state=12) #punto semilla con randomizacion
d2 = dataset
### Training
d3 = d2[0:int(cant_datos*train)]
d3["Species"] = [0 if value=="Iris-setosa" else value for value in list(d3["Species"])]
d3["Species"]= [1 if value=="Iris-versicolor" else value for value in list(d3["Species"])]
yram =d3["Species"]

inde_train_ram = pd.DataFrame({"x1":d3["sepal_len"],"x2":d3["sepal_wid"],
                           "x3":d3["petal_len"],"x4":d3["petal_wid"]})
depen_train_ram =pd.DataFrame({"y":d3["Species"]})


### TEST
d4 = d2[int(cant_datos*train):cant_datos]
d4["Species"] = [0 if value=="Iris-setosa" else value for value in list(d4["Species"])]
d4["Species"]= [1 if value=="Iris-versicolor" else value for value in list(d4["Species"])]
yram1 =d4["Species"]  #lo real

inde_test_ram = pd.DataFrame({"x11":d4["sepal_len"],"x22":d4["sepal_wid"],
                           "x33":d4["petal_len"],"x44":d4["petal_wid"]})
depen_test_ram =pd.DataFrame({"y1":d4["Species"]})

### Regresión Logística
#hclf = LogisticRegression(solver='lbfgs',random_state=1,multi_class="ovr")
reg2 = LogisticRegression(penalty='l1',solver='liblinear',random_state=1,multi_class="ovr")
ramdomcros=reg2.fit(inde_train_ram, depen_train_ram)

y_pred_ram=ramdomcros.predict(inde_test_ram) #preddicones
#print("Predicciones")
#print(y_pred_ram)
#print("Lo REAL")
#print(list(yram1))

from sklearn.metrics import confusion_matrix
print("Matriz de confusión")
print(confusion_matrix(yram1,y_pred_ram))


from sklearn.metrics import precision_score, recall_score,accuracy_score,f1_score
print("ACCURACY")
print(accuracy_score(yram1,y_pred_ram))
print("Recall")
print(recall_score(yram1, y_pred_ram)) #pos_label=1  q valor coger
print("Precision")
print(precision_score(yram1,y_pred_ram))
print("F1 Score")
print(f1_score(yram1,y_pred_ram))



