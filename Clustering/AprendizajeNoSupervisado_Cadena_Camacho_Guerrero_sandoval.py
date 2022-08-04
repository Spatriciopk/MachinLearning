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
from scipy.cluster.hierarchy import ClusterWarning
from warnings import simplefilter
simplefilter("ignore", ClusterWarning)
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
kmeans= modelo_kmeans.fit(X=dataset) #dataset original valores númericos
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



#########Crear Grupos: Jer�rquico#########
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import numpy as np


def plot_dendrogram(model, **kwargs):
    '''
    Esta función extrae la información de un modelo AgglomerativeClustering
    y representa su dendograma con la función dendogram de scipy.cluster.hierarchy
    '''
    
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count
   
    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot
    dendrogram(linkage_matrix, **kwargs)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
modelo_hclust_complete = AgglomerativeClustering(
                            affinity = 'euclidean',
                            linkage  = 'complete',
                            distance_threshold = None,
                            n_clusters         = 3,
                            compute_distances =True
                        )
modelo_hclust_complete.fit(X=dist_euclid)
arbol = modelo_hclust_complete.fit_predict(dist_euclid)
plot_dendrogram(modelo_hclust_complete,ax=ax)
labelsD = modelo_hclust_complete.labels_



######### Validacion Interna #########
# Indice de Dunn

import pandas as pd
from sklearn.metrics import davies_bouldin_score
print("Validación Interna")
print("Indice de DUNN")
print("Davies Bouldin Kmeans",davies_bouldin_score(dataset, labels))
print("Davies Bouldin  DHC",davies_bouldin_score(dataset, labelsD))



####### Indice de silueta

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
import numpy as np
from matplotlib import cm
from sklearn.metrics import silhouette_score,silhouette_samples
cluster_labels=np.unique(kmeans2)
n_clusters=cluster_labels.shape[0]
silhouette_vals=silhouette_samples(dist_euclid,kmeans2,metric='precomputed')#poner en precomputed
y_ax_lower,y_ax_upper=0,0
yticks=[]
lend=""
lista_clusters_l =list(labels)
clus1 = lista_clusters_l.count(0)
clus2 = lista_clusters_l.count(1)
clus3 = lista_clusters_l.count(2)
clus = [clus1,clus2,clus3]
for i,c in enumerate(cluster_labels):
    c_silhouette_vals=silhouette_vals[kmeans2==c]
   
    c_silhouette_vals.sort()
    silhouette_avg=np.mean(c_silhouette_vals)
   
    
    y_ax_upper+=len(c_silhouette_vals)
    color=cm.jet(float(i)/n_clusters)
    plt.barh(range(y_ax_lower,y_ax_upper),
             c_silhouette_vals,
             height=1.0,
             edgecolor='none',
             color=color)
  
    lend=lend+ str(clus[i])+"|" + str(round(silhouette_avg,2)) +","
    yticks.append((y_ax_lower+y_ax_upper)/2.0)
    y_ax_lower+=len(c_silhouette_vals)
   

silhouette_avg=np.mean(silhouette_vals) #media o averegue del silueta
plt.axvline(silhouette_avg,
            color='black',
            linestyle='--')

lend = lend.split(",")
aux = round(silhouette_avg,2)

lend.pop(len(lend)-1)
lend.insert(0, aux)
plt.legend(lend)
plt.yticks(yticks,cluster_labels+1)
plt.ylabel("Cluster")
plt.xlabel("Silhouette Coefficients Kmeans")
plt.show()
#print(silhouette_score_cluster_3) #promedio 
print("El promedio o Average solhouette witdh KMeans: ", silhouette_avg)
#print(n_clusters)
#print(cluster_labels)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

cluster_labels=np.unique(arbol)
n_clusters=cluster_labels.shape[0]
silhouette_vals=silhouette_samples(dist_euclid,arbol,metric='precomputed')#poner en precomputed
y_ax_lower,y_ax_upper=0,0
yticks=[]
lend=""
lista_clusters_l =list(labelsD)
clus1 = lista_clusters_l.count(0)
clus2 = lista_clusters_l.count(1)
clus3 = lista_clusters_l.count(2)
clus = [clus1,clus2,clus3]
for i,c in enumerate(cluster_labels):
    c_silhouette_vals=silhouette_vals[arbol==c]
   
    c_silhouette_vals.sort()
    silhouette_avg=np.mean(c_silhouette_vals)
   
    
    y_ax_upper+=len(c_silhouette_vals)
    color=cm.jet(float(i)/n_clusters)
    plt.barh(range(y_ax_lower,y_ax_upper),
             c_silhouette_vals,
             height=1.0,
             edgecolor='none',
             color=color)
  
    lend=lend+ str(clus[i])+"|" + str(round(silhouette_avg,2)) +","
    yticks.append((y_ax_lower+y_ax_upper)/2.0)
    y_ax_lower+=len(c_silhouette_vals)
   

silhouette_avg=np.mean(silhouette_vals)
plt.axvline(silhouette_avg,
            color='black',
            linestyle='--')

lend = lend.split(",")
aux = round(silhouette_avg,2)

lend.pop(len(lend)-1)
lend.insert(0, aux)
plt.legend(lend)
plt.yticks(yticks,cluster_labels+1)
plt.ylabel("Cluster")
plt.xlabel("Silhouette Coefficients DHC")
plt.show()
print("El promedio o Average solhouette witdh DHC: ", silhouette_avg)






#Validacion Externa
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import normalized_mutual_info_score
lista_especies = list(iris_es)
lista_labels = list(labels)
lista_labelsD = list(labelsD)
ariK = adjusted_rand_score(lista_especies, lista_labels)
ariD = adjusted_rand_score(lista_especies, lista_labelsD)
print()
print("Validación Externa")
print("ARI Kmeans",ariK)
print("ARI DHC",ariD)
amiK = adjusted_mutual_info_score(lista_especies, lista_labels)
amiD = adjusted_mutual_info_score(lista_especies, lista_labelsD)
print("AMI Kmeans",amiK)
print("AMI DHC",amiD)
nmiK = normalized_mutual_info_score(lista_especies, lista_labels)
nmiD = normalized_mutual_info_score(lista_especies, lista_labelsD)
print("NMI Kmeans",nmiK)
print("NMI DHC",nmiD)