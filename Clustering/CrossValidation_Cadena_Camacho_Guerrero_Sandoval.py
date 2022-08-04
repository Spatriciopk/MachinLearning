#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 19:11:01 2022

@author: spatricio
"""

#Cross Validation


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



###########################Houldt Method######################################
### Training

d1 = dataset[0:int(cant_datos*train)]



x1 = d1["sepal_len"]
x2 = d1["sepal_wid"]
x3 = d1["petal_len"]
x4 = d1["petal_wid"]
d1["Species"] = [0 if value=="Iris-setosa" else value for value in list(d1["Species"])]
d1["Species"]= [1 if value=="Iris-versicolor" else value for value in list(d1["Species"])]
y =d1["Species"]

inde_train = pd.DataFrame({"x1":d1["sepal_len"],"x2":d1["sepal_wid"],
                           "x3":d1["petal_len"],"x4":d1["petal_wid"]})
depen_train =pd.DataFrame({"y":d1["Species"]})


### TEST

d1 = dataset[int(cant_datos*train):cant_datos]
x11 = d1["sepal_len"]
x22 = d1["sepal_wid"]
x33 = d1["petal_len"]
x44 = d1["petal_wid"]
d1["Species"] = [0 if value=="Iris-setosa" else value for value in list(d1["Species"])]
d1["Species"]= [1 if value=="Iris-versicolor" else value for value in list(d1["Species"])]
y1 =d1["Species"]

inde_test = pd.DataFrame({"x11":d1["sepal_len"],"x22":d1["sepal_wid"],
                           "x33":d1["petal_len"],"x44":d1["petal_wid"]})
depen_test =pd.DataFrame({"y1":d1["Species"]})

### Regresión Logística
#hclf = LogisticRegression(solver='lbfgs',random_state=1,multi_class="ovr")
reg = LogisticRegression(penalty='l1',solver='liblinear',random_state=1,multi_class="ovr")

houldt=reg.fit(inde_train, depen_train)

y_pred=houldt.predict(inde_test) #preddicones
#print(y_pred)
#COEFICIENTES DE LA REGRESION
b0=houldt.intercept_[0]
b1=houldt.coef_[0,0]
b2=houldt.coef_[0,1]
b3=houldt.coef_[0,2]
b4=houldt.coef_[0,3]


yestr=np.exp(b0+b1*x11+b2*x22+b3*x33+b4*x44)/(1+np.exp(b0+b1*x11+b2*x22+b3*x33+b4*x44))
yestr2 = round(yestr)
#print(yestr2)
rate_error = (yestr2 == y1)*1
accuracy=sum(rate_error)/len(y1)
print("HOLDOUT METHOD")
print('Accuracy',accuracy)

###########################Random Cross-Validation######################################




d2 = dataset.sample(cant_datos,random_state=12) #punto semilla con randomizacion

### Training
d3 = d2[0:int(cant_datos*train)]



xram1 = d3["sepal_len"]
xram2 = d3["sepal_wid"]
xram3 = d3["petal_len"]
xram4 = d3["petal_wid"]
d3["Species"] = [0 if value=="Iris-setosa" else value for value in list(d3["Species"])]
d3["Species"]= [1 if value=="Iris-versicolor" else value for value in list(d3["Species"])]
yram =d3["Species"]

inde_train_ram = pd.DataFrame({"x1":d3["sepal_len"],"x2":d3["sepal_wid"],
                           "x3":d3["petal_len"],"x4":d3["petal_wid"]})
depen_train_ram =pd.DataFrame({"y":d3["Species"]})



### TEST

d4 = d2[int(cant_datos*train):cant_datos]
xram11 = d4["sepal_len"]
xram22 = d4["sepal_wid"]
xram33 = d4["petal_len"]
xram44 = d4["petal_wid"]
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
#print(y_pred)
#COEFICIENTES DE LA REGRESION
b0ram=ramdomcros.intercept_[0]
b1ram=ramdomcros.coef_[0,0]
b2ram=ramdomcros.coef_[0,1]
b3ram=ramdomcros.coef_[0,2]
b4ram=ramdomcros.coef_[0,3]


yestram=np.exp(b0ram+b1ram*xram11+b2ram*xram22+b3ram*xram33+b4ram*xram44)/(1+np.exp(b0ram+b1ram*xram11+b2ram*xram22+b3ram*xram33+b4ram*xram44))
yestram2 = round(yestram) #lo predicho o prediccion
#print(yestr2)
rate_error_ram = (yestram2 == yram1)*1
accuracyram=sum(rate_error_ram)/len(yram1)
print()
print("Random Cross-Validation")
print('Accuracy',accuracyram)



###########################K-Fold Cross-Validation######################################

k = 10
k_fold = KFold(n_splits=k)


d5 = dataset[0:cant_datos]
values_inde = pd.DataFrame({"x1": d5['sepal_len'],
                   "x2": d5['sepal_wid'],
                   "x3": d5['petal_len'],
                   "x4": d5['petal_wid'] })


d5["Species"] = [0 if value=="Iris-setosa" else value for value in list(d5["Species"])]
d5["Species"]= [1 if value=="Iris-versicolor" else value for value in list(d5["Species"])]
d5["Species"] =d5["Species"] 
values_dep = pd.DataFrame({"y": d5['Species']})
y_dep = values_dep.to_numpy()

reg3 = LogisticRegression(penalty='l1',solver='liblinear',random_state=1,multi_class="ovr")
list_acurracy = []

for train,test in k_fold.split(values_inde):
    xtr= values_inde.iloc[train,:]
    ytr= y_dep[train]
    xtest= values_inde.iloc[test,:]
    ytest= y_dep[test]
    reg3.fit(xtr,ytr)
    predic = reg3.predict(xtest)
    list_acurracy.append(accuracy_score(predic,ytest))
print()
print("K-Fold Cross-Validation with k = 10")
print("TODOS LOS MODELOS")
print(list_acurracy)
print("Accuracy: ", sum(list_acurracy)/k)
    


###########################Leave-one-out Cross-Validation######################################

d6 = dataset[0:cant_datos]
values_inde_l = pd.DataFrame({"x1": d6['sepal_len'],
                   "x2": d6['sepal_wid'],
                   "x3": d6['petal_len'],
                   "x4": d6['petal_wid'] })

values_dep_l = pd.DataFrame({"y": d5['Species']})
locv = LeaveOneOut() # (p=2) número de iteraciones
valor_real = list()
valor_pred = list()
reg4 = LogisticRegression(penalty='l1',solver='liblinear',random_state=1,multi_class="ovr")
for train,test in locv.split(values_inde_l.to_numpy()):
    xtr= values_inde.iloc[train,:]
    ytr= y_dep[train]
    
    xtest= values_inde.iloc[test,:]
    ytest= y_dep[test]
    reg4.fit(xtr,ytr)
    predic= reg4.predict(xtest)
    valor_real.append(ytest[0])
    valor_pred.append(predic[0])

print()
print("Leave-one-out Cross-Validation")
print("Accuracy",accuracy_score(valor_real, valor_pred))