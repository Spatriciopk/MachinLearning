#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 22:07:37 2022

@author: spatricio
"""


import pandas as pd
from sklearn.cluster import KMeans

      

from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
from sklearn import datasets
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import numpy as np
from scipy.cluster.hierarchy import ClusterWarning
from warnings import simplefilter
from sklearn.metrics import davies_bouldin_score
from matplotlib import cm
from sklearn.metrics import silhouette_score,silhouette_samples
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import normalized_mutual_info_score
from warnings import simplefilter
from scipy.cluster.hierarchy import ClusterWarning
import warnings
simplefilter("ignore", ClusterWarning)
warnings.filterwarnings("ignore")
df = pd.read_csv("segmentation_data.csv")
df = pd.DataFrame(df)
del df["client"]
df = df.iloc[:,[0,1,2]]
print("Data Set")
print(df)

##Literal 1
dist_euclid = euclidean_distances(df) 

modelo_kmeans = KMeans(n_clusters=4,random_state=1)
kmeans= modelo_kmeans.fit(X=df)
kmeans2 = modelo_kmeans.fit_predict(df)
labels = kmeans.predict(df) #se encuentran los cluster la lista
lista_clusters_l =list(labels)
clus1 = lista_clusters_l.count(0)
clus2 = lista_clusters_l.count(1)
clus3 = lista_clusters_l.count(2)
clus4 = lista_clusters_l.count(3)
#list_a= [clus1,clus2,clus3,clus4]
#lista_aux = sorted(list_a)


print("###################### Literal 1 ##############################")

print("Se considera escoger con VIP al Grupo: 1, pues el dataset existen muy pocos clientes con un número de frecuencia alto y un número de recenty bajo, ademas de un grado aporte economico al establecimiento ")
print("Se considera escoger con NUEVOS al Grupo: 2, pues el dataset existen clientes con un aporte economico bajo lo que indica clientes nuevos, en el data set son pocos")
print("Se considera escoger con Vip_potencial al Grupo: 0, pues en el data set existen varios clientes potenciales por encima de clientes nuevos, tienen una una frecuencia,recenty y aporte economico por debajo de los clientes VIP, son varios")
print("Se considera escoger con Baja_Frecuencia al Grupo: 3, pues en el data set existen muchos clientes con poca frecuencia y un recenty muy elevado ,")
print()
print("K-Means ")
#print("Grupos: ",lista_clusters_l)
print("VIP: ",clus2)
print("NUEVOS: ",clus3)
print("VIP_POTENCIAL: ",clus4)
print("BAJA FRECUENCIA: ",clus1)
#print("VIP: ",lista_aux[0])
#print("NUEVOS: ",lista_aux[1])
#print("VIP_POTENCIAL: ",lista_aux[2])
#print("BAJA FRECUENCIA: ",lista_aux[3])
#########Crear Grupos: Jer�rquico#########
modelo_hclust_complete = AgglomerativeClustering(
                            affinity = 'euclidean',
                            linkage  = 'complete',
                            distance_threshold = None,
                            n_clusters         = 4,
                            compute_distances =True
                        )
modelo_hclust_complete.fit(X=dist_euclid)
arbol = modelo_hclust_complete.fit_predict(dist_euclid)
labelsD = modelo_hclust_complete.labels_

lista_clusters_D =list(labelsD)
clus5 = lista_clusters_D.count(0)
clus6 = lista_clusters_D.count(1)
clus7 = lista_clusters_D.count(2)
clus8 = lista_clusters_D.count(3)
list_a= [clus5,clus6,clus7,clus8]
lista_aux = sorted(list_a)
print()
print("DHC ")
#print("Grupos: ",lista_clusters_D)
print("VIP: ",lista_aux[0])
print("NUEVOS: ",lista_aux[1])
print("VIP_POTENCIAL: ",lista_aux[2])
print("BAJA FRECUENCIA: ",lista_aux[3])

###Literal 2
#Comparar el rendimiento de los resultados del literal anterior mediante TODAS
#las métricas que conoce
print()
print("###################### Literal 2 ##############################")
print("Validación Interna")
print("Indice de DUNN")
print("Davies Bouldin Kmeans",davies_bouldin_score(df, labels))
print("Davies Bouldin  DHC",davies_bouldin_score(df, labelsD))
print("Indice de silueta")

####### Indice de silueta
silhouette_vals=silhouette_samples(dist_euclid,kmeans2,metric='precomputed')#poner en precomputed
silhouette_avg=np.mean(silhouette_vals) #media o averegue del silueta
print("Silhouette witdh KMeans: ", silhouette_avg)

silhouette_vals=silhouette_samples(dist_euclid,arbol,metric='precomputed')#poner en precomputed
silhouette_avg=np.mean(silhouette_vals) #media o averegue del silueta
print("Silhouette witdh DHC: ", silhouette_avg)

##LITERAL3
##Tomando en cuenta como “ground truth” el resultado del primer algoritmo,
#indique qué tan bueno es el rendimiento del segundo algoritmo (2 puntos).
print()
print(" ###################### Literal 3 ##############################")
#Validacion Externa
lista_labels = list(labels)
lista_labelsD = list(labelsD)
print()
print("Validación Externa")
ariD = adjusted_rand_score(lista_labels, lista_labelsD)
print("ARI DHC",ariD)
amiD = adjusted_mutual_info_score(lista_labels, lista_labelsD)
print("AMI DHC",amiD)
nmiD = normalized_mutual_info_score(lista_labels, lista_labelsD)
print("NMI DHC",nmiD)
