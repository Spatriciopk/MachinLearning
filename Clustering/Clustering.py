#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 18:58:32 2022

@author: spatricio
"""

#Escalamiento multidimensional

import pandas as pd

from sklearn.manifold import MDS
from matplotlib import pyplot as plt

import seaborn as sns         

from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances

iris = pd.read_csv("Iris.csv")
print(iris)
iris = pd.DataFrame(iris)
iris_es = iris["Species"]
del iris["Species"]
del iris["Id"]

def mapData(dist_matrix, metric, title,iris_es):
    mds = MDS(2,metric=metric, dissimilarity='precomputed', random_state=0)
    pts = mds.fit_transform(dist_matrix)       # Plot the embedding, colored according to the class of the points
    fig = plt.figure(1, (15,6))
    ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1],hue=iris_es, palette=['r', 'g', 'b'])
    plt.title(title)    
    plt.show()
    

dist_euclid = euclidean_distances(iris) 
mapData(dist_euclid, True, 
        'Metric MDS with Euclidean',iris_es)


#########Crear Grupos: K-Means########
from sklearn.cluster import KMeans
mds = MDS(2,metric=True, dissimilarity='precomputed', random_state=0)
pts = mds.fit_transform(dist_euclid)  

modelo_kmeans = KMeans(n_clusters=3)
kmeans= modelo_kmeans.fit(X=iris)
kmeans2 = modelo_kmeans.fit_predict(iris)
labels = kmeans.predict(iris) #se encuentran los cluster
colores=['red','green','blue']
asignar=[]
for row in labels:
    asignar.append(colores[row])

fig = plt.figure(1, (15,6))
ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1],hue=asignar, palette=['r', 'g','b'])
plt.title("Cluster")    
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


######### Elbow #########
# Crea diferentes valores de k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(iris)
    distortions.append(kmeanModel.inertia_)
    
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('Número de Clusters')
plt.ylabel('Suma de cuadrados internos')
plt.title('The Elbow Method showing the optimal k')
plt.show()


######### Validacion Interna #########
# Indice de Dunn




import pandas as pd
from sklearn.metrics import davies_bouldin_score
print()
print("Coeficiente de davies bouldin kmeans",davies_bouldin_score(iris, labels))
print("Coeficiente de davies bouldin dhc",davies_bouldin_score(iris, labelsD))



# Coeficiente de Silueta
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
plt.xlabel("Silhouette Coefficients Kmeans")
plt.show()
#print(silhouette_score_cluster_3) #promedio 
#print("El promedio o Average solhouette witdh : ", silhouette_avg)
#print(n_clusters)
#print(cluster_labels)



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


#Validacion Externa
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import normalized_mutual_info_score
lista_especies = list(iris_es)
lista_labels = list(labels)
lista_labelsD = list(labelsD)
ariK = adjusted_rand_score(lista_especies, lista_labels)
ariD = adjusted_rand_score(lista_especies, lista_labelsD)
#print(lista_especies)
#print(lista_labels)
#print(lista_labelsD)
print()
print("ARI Kmeans",ariK)
print("ARI DHC",ariD)
print()
amiK = adjusted_mutual_info_score(lista_especies, lista_labels)
amiD = adjusted_mutual_info_score(lista_especies, lista_labelsD)
print("AMI Kmeans",amiK)
print("AMI DHC",amiD)
print()
nmiK = normalized_mutual_info_score(lista_especies, lista_labels)
nmiD = normalized_mutual_info_score(lista_especies, lista_labelsD)
print("NMI Kmeans",nmiK)
print("NMI DHC",nmiD)
