#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 19:34:44 2022

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
from sklearn.linear_model import LinearRegression
import numpy as np
import random
from random import sample
from sklearn.model_selection import KFold
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import train_test_split
warnings.filterwarnings("ignore")
iris = datasets.load_iris()
iris_df=pd.DataFrame(iris.data)
iris_df['Species']=iris.target
iris_df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'Species']
iris_df.dropna(how="all", inplace=True) # remove any empty lines
iris_X=iris_df.iloc[:,[0,1,2,3,4]]

train = 0.7
test = 1- train
cant_datos =150
#Randomizamos con semilla y sample

dataset=iris_X.iloc[:,[0,1,2,3,4]]

###########################Random Cross-Validation######################################
#dataset =iris_X.iloc[:,[0,1,2,3]]
#dataset_y =iris_X.iloc[:,[4]]

dataset = iris_X.sample(cant_datos,random_state=12) #punto semilla con randomizacion
#dataset = iris_X

### Training
d3 = dataset[0:int(cant_datos*train)]

input_cols_train =["sepal_len","sepal_wid","petal_len"]
output_var_train =["petal_wid"]
X_train = d3[input_cols_train]
y_train = d3[output_var_train]

#X_train,X_test,y_train,y_test=train_test_split(dataset,dataset_y,train_size=train,random_state=12)


### TEST

d4 = dataset[int(cant_datos*train):cant_datos]

input_cols_test =["sepal_len","sepal_wid","petal_len"]
output_var_test =["petal_wid"]
X_test = d4[input_cols_test]
y_test = d4[output_var_test]




reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred_ram=reg.predict(X_test)
from numpy import mean
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import math
error = y_test - y_pred_ram
#print("Error")
#print(error["petal_wid"])
SCE = sum(error["petal_wid"]**2)
print("SCE: ",SCE)
y_med = mean(y_test["petal_wid"])
STC= sum((y_test["petal_wid"]-y_med)**2)
print("STC: ",STC)
SCR = STC -SCE
print("SCR: ",SCR)
r2 = SCR/STC
print("R-cuadrado: ",r2)
r2a = 1-(1-r2)*((len(y_test)-1)/(len(y_test)-(len(reg.coef_))-1))
print("R-cuadrado ajustado: ",r2a)
MAE=mean_absolute_error(y_test, y_pred_ram, multioutput='raw_values')
print("MEAN ABSOLUTE ERROR: ",MAE[0])
MSE=mean_squared_error(y_test, y_pred_ram, multioutput='raw_values')
print("MEAN SQUARE ERROR: ",MSE[0])
RSME = math.sqrt(MSE)
print("ROOT MEAN SQUARE ERROR: ",RSME)


#print(reg.coef_)

###Resumen de la regresion
#import statsmodels.api as sm
#X_const =sm.add_constant(X_train,prepend=True)
#model = sm.OLS(endog=y_train, exog=X_train).fit()

#view model summary
#print(model.summary())
#print(model.predict())
