#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 22:20:50 2022

@author: spatricio
"""

import pandas as pd

from sklearn.manifold import MDS
from matplotlib import pyplot as plt

import seaborn as sns         

from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
from sklearn import datasets
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

dataset=iris_df.iloc[:,[0,1,2,3]]

#########Crear Grupos: K-Means########
dist_euclid = euclidean_distances(dataset) 
from sklearn.cluster import KMeans
mds = MDS(3,metric=True, dissimilarity='precomputed', random_state=0)
pts = mds.fit_transform(dist_euclid)  

modelo_kmeans = KMeans(n_clusters=3)
kmeans= modelo_kmeans.fit(X=dataset)
kmeans2 = modelo_kmeans.fit_predict(dataset)
labels = kmeans.predict(dataset) #se encuentran los cluster
lista_clusters_l =list(labels)
clus1 = lista_clusters_l.count(0)
clus2 = lista_clusters_l.count(1)
clus3 = lista_clusters_l.count(2)
colores=['Iris-setosa: '+str(clus1) ,'Iris-versicolor: '+str(clus2),'Iris-virginica: '+str(clus3)]
asignar=[]
for row in labels:
    asignar.append(colores[row])
    
fig = plt.figure(1, (15,6))
ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1],hue=asignar, palette=['r', 'g','b'])

plt.title("K-Means")    
plt.show()



######### Elbow #########
# Crea diferentes valores de k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(dataset)
    distortions.append(kmeanModel.inertia_)
    
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('Número de Clusters')
plt.ylabel('Suma de cuadrados internos')
plt.title('The Elbow Method showing the optimal k')
plt.show()




