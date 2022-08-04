#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:03:10 2022

@author: spatricio
"""

import re
import nltk  
import pandas as pd
from pandas import *
import csv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import defaultdict
import numpy as np
import math
import time

n = stopwords.words("english")
stemmer = PorterStemmer()
def importacion_columnas(columna):
    data = read_csv("paper.csv")
    columna = data[columna].tolist()
    return columna


df = pd.read_csv("ICMLA_2014_2015_2016_2017.csv")
df = pd.DataFrame(df)
del df["paper_id"]
del df["year"]
df_group = df["session"]

#titulos = importacion_columnas("title")
#keywords = importacion_columnas("keywords")
#abstract = importacion_columnas("abstract")

def minusculas(lista):
    tit = []
    for token in lista:
        tit.append(token.lower())
    return tit

def caracter_especiales(lista):
    tit = []
    for token in lista:
        #for caracter in token:
        tit.append(re.sub('[^A-Za-z0-9]+', ' ', token))
        
    return tit

#Normalizacion

titulos = caracter_especiales(list(df["title"]))
titulos = minusculas(titulos)

keywords = caracter_especiales(list(df["keywords"]))
keywords = minusculas(keywords)

abstract = caracter_especiales(list(df["abstract"]))
abstract = minusculas(abstract)

def tokenizacion(lista):
    tit = []
    aux = []
    for token in lista:
        aux.append(token.split())   
    tit = aux
    return tit

def comprobar_stop_words(lista):
    global n
    for cadena in lista:
        for word in cadena:
            if (word in n):
               return True
    return False

def eliminar_stop_words(lista):
    global n
    while (comprobar_stop_words(lista)):
        for cadena in lista:
            for word in cadena:
                if (word in n):
                    cadena.remove(word)
    return lista

def stemming(lista):
    global stemmer
    tit = []
    aux = []
    for cadena in lista:
        aux = []
        for token in cadena:
            aux.append(stemmer.stem(token))
        tit.append(aux)
    return tit

#Tokenizacion

titulos = tokenizacion(titulos)
keywords = tokenizacion(keywords)
abstract = tokenizacion(abstract)

#Stopwords
titulos = eliminar_stop_words(titulos)
keywords = eliminar_stop_words(keywords)
abstract = eliminar_stop_words(abstract)

#Stemming
titulos = stemming(titulos)
keywords = stemming(keywords)
abstract = stemming(abstract)

#separacion de grupos
def grupos(df_group,lista_group):
    df_group = list(df_group)
    df_group = minusculas(df_group)
    df_group = caracter_especiales(df_group)
    for grupo in df_group:
        if grupo.rstrip() not in lista_group:
            lista_group.append(grupo.rstrip())

lista_group = []
grupos(df_group, lista_group)
num_grupos = len(lista_group)

#from collections import Counter
#labels = list(Counter(lista_group).keys())
#print(len(labels))

def jacard (titulos,matriz):
    union = []
    aux = []
    interseccion = []
    cont = 0
    vector = []
    palabras_unidas =""
    vectoraux_titulos=[]
    vector_titulos = []
    #Se eliminan las palabras repetidas
    for lista in titulos:
        for palabra in lista:
            if palabra not in vectoraux_titulos:
                vectoraux_titulos.append(palabra)
       
        vector_titulos.append(vectoraux_titulos)
        vectoraux_titulos = []
    
    #se vuelve a unir las palabras
    for frase in vector_titulos:
        for palabra in frase:
            if ( palabras_unidas ==""):
                palabras_unidas = palabra
            else:
                palabras_unidas = palabras_unidas +" " +palabra
        vector.append(palabras_unidas)
        palabras_unidas = ""

    for i in range(len(vector)-1):
        for j in range(i+1,len(vector)):
            frase=""
            lista = []
            frase = vector[i] +" "+ vector[j]
            nueva_frase = ""
            lista = frase.split(" ")
            aux.append(len(lista))
           
            for element in lista:
               if element not in nueva_frase:
                   nueva_frase= nueva_frase +" "+element
            lista =nueva_frase.split(" ")
            lista.pop(0)
            union.append(len(lista))
            interseccion.append(aux[cont]- len(lista))
            cont +=1
    indice =0
    for i in range(len(matriz[1])):
        for j in range(len(matriz[1])):
            if (j > i):
                matriz[i][j]=round(interseccion[indice]/union[indice],2)
                indice +=1
    for i in range(len(matriz[1])):
         for j in range(len(matriz[1])):
             if (j < i):  
                matriz[i][j] = matriz[j][i]
    
def llenar_identidad(matriz):
    for i in range(len(matriz[1])):
        for j in range(len(matriz[1])):
            if(i == j):
                matriz[i][j]=1


matriz_titulos = np.zeros((len(titulos), len(titulos))) #Matriz de distancias titulos
matriz_keywords = np.zeros((len(keywords), len(keywords))) #Matriz de distancias keywords
llenar_identidad(matriz_titulos)
llenar_identidad(matriz_keywords)
jacard(titulos,matriz_titulos)
jacard(keywords,matriz_keywords)


############################# Matriz de distancias abstract

vocabulario = []

def generar_vocabulario(documentos,vocabulario):
    for documento in documentos:
        for palabra in documento:
            if(palabra not in vocabulario):
                vocabulario.append(palabra)
                
generar_vocabulario(abstract, vocabulario)
matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
frecuencia = []

def frecuencias (vocabulario,abstract,frecuencia):
    lista_aux = []
  
    for lista in abstract:
        for palabra in vocabulario:
                lista_aux.append(lista.count(palabra))
        frecuencia.append(lista_aux)
        lista_aux = []
def llenar_palabras_documentos (vocabulario,abstract,matriz_df_idf):
    for i in range(len(matriz_df_idf)):
        
        for j in range(len(matriz_df_idf[1])):
            if(j== 0):
                if(i == 0):
                    matriz_df_idf[i][j]= "Terminos"
                else:
                    matriz_df_idf[i][j]= str(vocabulario[i-1])
            if(i==0 and j!=0):
                matriz_df_idf[i][j]= "Doc: "+ str(j)

def llenar_matriz (frecuencia,matriz_df_idf,texto):
    for i in range(len(frecuencia)):
        for j in range (len(frecuencia[i])):
            matriz_df_idf[j+1][i+1] = texto +str(frecuencia[i][j])
def llenar_matriz2 (frecuencia,matriz_df_idf,texto):
    
    for i in range(len(frecuencia)):
            matriz_df_idf[i+1][1] = texto +str(frecuencia[i])

def calcular_wtf (frecuencia,lista_wtf):
    lista_aux = []
    for lista_frecuencia in frecuencia:
        for dato in lista_frecuencia:
            if(dato > 0):
                lista_aux.append(round((math.log(dato,10))+1,2))
            else:
                lista_aux.append(0)
        lista_wtf.append(lista_aux)
        lista_aux=[]

def calcular_df (lista_wtf,lista_df,vocabulario):
    cont = 0
    index = 0
    for rep in range(len(vocabulario)):
        for lista in lista_wtf:
            if(lista[index]>0):
                cont+=1
        index+=1
        lista_df.append(cont)
        cont=0
def calcular_idf (lista_df,abstract,lista_idf):
    for dato in lista_df:
        #lista_idf.append(round(math.log(3/dato,10),2))
        lista_idf.append(round(math.log(len(abstract)/dato,10),2))

def calcular_Tf_Idf(lista_idf,lista_wtf,lista_tf_idf):
    for lista in lista_wtf:
        lista_tf_idf.append(np.multiply(lista,lista_idf))
     
def redondear(lista_tf_idf):
   lista = []
   lista_aux =[]
   for i in range(len(lista_tf_idf)):
       for j in range (len(lista_tf_idf[i])):
           lista_aux.append(round(lista_tf_idf[i][j],2))
       lista.append(lista_aux)
       lista_aux = []
   return lista


    
def modulo_raiz(lista_wtf,lista_modulo,vocabulario):
   
    acum = 0

    for lista in lista_wtf:
        for dato in lista:
            if(dato>0):
               acum = acum + dato**2
        lista_modulo.append(round(math.sqrt(acum),2))
        acum=0

def lista_normalizada(lista_wtf,lista_modulo,lista_normal):
    indice = 0
    for lista in lista_wtf:
        lista_normal.append(list(map(lambda x: x / lista_modulo[indice],lista)))
        indice+=1

def retorno_lista (array_lista):
    lista = []
    lista_aux= []
    for dato in array_lista:
        for lt in dato:
            lista_aux.append(lt)
        lista.append(lista_aux)
        lista_aux= []
    return lista

def matriz_distancia_abstrac(lista_normal,lista_abstract_final):
    lista_aux=[]
    for i in range(len(lista_normal)-1):
        for j in range(i+1,len(lista_normal)):
            lista_aux.append(np.multiply(lista_normal[i],lista_normal[j]))
        nueva = retorno_lista(lista_aux)
        for i in range(len(nueva)):
            lista_abstract_final.append(round(sum(nueva[i]),2))
        lista_aux=[]

def llenar_matriz_Distancias (matriz_distancia_abs):
    for i in range(len(matriz_distancia_abs)):
        for j in range(len(matriz_distancia_abs[1])):
            if( i== j ):
                matriz_distancia_abs[i][j]=1
                
def llenar_valores_matriz_Distancias(matriz_distancia_abs,lista_abstract_final):
    indice=0
    #print(len(matriz_distancia_abs)) len(matriz_distancia_abs)
    #print(len(lista_abstract_final)) len(matriz_distancia_abs[1])
    for i in range(0,len(matriz_distancia_abs)):
        for j in range(0,len(matriz_distancia_abs[1])):
            if (j > i):
                matriz_distancia_abs[i][j] =lista_abstract_final[indice]
                indice+=1
def llenar_valores_matriz_Distancias_re(matriz_distancia_abs,lista_abstract_final):

    indice=0
    for i in range(0,len(matriz_distancia_abs)):
        for j in range(0,len(matriz_distancia_abs[1])): 
            if (i < j):
                matriz_distancia_abs[j][i] =lista_abstract_final[indice]
                indice+=1
        
lista_wtf = [] 
lista_df = []   
lista_idf = []  
lista_tf_idf = []  
lista_modulo = [] 
lista_normal = []   
lista_abstract_final =[]   
frecuencias(vocabulario, abstract,frecuencia)
#llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
#llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
#print("#########Term Frecuency#############")
#print(matriz_df_idf)
#print()
#print("#########Weight Document Frecuency#############")
matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
calcular_wtf(frecuencia, lista_wtf)
#llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
#llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
#print(matriz_wtf)
#print()
#print("#########Document Frecuency#############")
matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
calcular_df(lista_wtf, lista_df,vocabulario)
#llenar_palabras_documentos(vocabulario, abstract, matriz_df)
#llenar_matriz2(lista_df,matriz_df,"DF: ")
#print(matriz_df)
#print()
#print("#########Inverse Document Frecuency#############")
matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
calcular_idf(lista_df, abstract, lista_idf)
#llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
#llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
#print(matriz_idf)
#print()
#print("######### TF - IDF#############")
matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
lista_tf_idf =redondear(lista_tf_idf)
#llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
#llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
#print(matriz_tf_idf)
#print()
#print("######### Matriz de distancias abstract #############")
####Modulo de la raiz normalizacion
modulo_raiz(lista_wtf, lista_modulo, vocabulario)
lista_normalizada(lista_wtf, lista_modulo,lista_normal)
lista_normal =redondear(lista_normal)

###### Matriz de distancias Abstract #######

matriz_distancia_abstrac(lista_normal,lista_abstract_final)
matriz_distancia_abs = np.zeros((len(abstract),len(abstract)))
llenar_matriz_Distancias(matriz_distancia_abs)
llenar_valores_matriz_Distancias(matriz_distancia_abs,lista_abstract_final)
llenar_valores_matriz_Distancias_re(matriz_distancia_abs,lista_abstract_final)
#print("Matriz de distancia abstract")
#print(matriz_distancia_abs)
#print()
#print("##### Matriz de distancias de titulos con 20%  ########")
matriz_tit_20 = np.around(np.matrix(matriz_titulos*0.20),2)
#print(matriz_tit_20)
#print()
#print("##### Matriz de distancias de keywords con 30%  ########")
matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
#print(matriz_key_30)
#print()
#print("######### Matriz de distancias abstract 50%#############")
matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
#print(matriz_abs_50)
matriz_aux = np.add(matriz_tit_20,matriz_key_30)

matriz_resultante = np.add(matriz_aux,matriz_abs_50)
print("########## LITERAL 1 #################")
print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstract #############")
print(matriz_resultante)




##########Creando grupos por DHC
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import numpy as np
from matplotlib import pyplot as plt


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
                            affinity = 'precomputed',
                            linkage  = 'complete',
                            distance_threshold = None,
                            n_clusters         = num_grupos,
                            compute_distances =True
                        )
modelo_hclust_complete.fit(X=matriz_resultante)
arbol = modelo_hclust_complete.fit_predict(matriz_resultante)
plot_dendrogram(modelo_hclust_complete,ax=ax)
labelsD = modelo_hclust_complete.labels_

from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
dist_euclid = euclidean_distances(matriz_resultante) 

print()
print("Número de grupos :", num_grupos)

######### Validacion Interna #########
# Indice de Dunn

#!pip install validclust
from validclust import dunn

du2 = dunn(dist_euclid,labelsD)
print()
print("Validación Interna")
print('Índice de Dunn con DHC: %.5f' % du2)

#########################################################################


# Coeficiente de Silueta

#matriz_resultante = np.around(np.matrix(1- matriz_resultante),2)

#print(dist_euclid)
from matplotlib import cm
from sklearn.metrics import silhouette_score,silhouette_samples
fig, ax = plt.subplots(1, 1, figsize=(8, 4))

cluster_labels=np.unique(arbol)
n_clusters=cluster_labels.shape[0]
silhouette_vals=silhouette_samples(dist_euclid,arbol,metric='precomputed')#poner en precomputed
y_ax_lower,y_ax_upper=0,0
yticks=[]
lend=""
lista_clusters_l =list(labelsD)

def lista_clus (lista_clusters_l):
    aux = []
    for i in range(num_grupos):
        aux.append(lista_clusters_l.count(i))
    return aux

clus = lista_clus(lista_clusters_l)

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
print("Average silhouette witdh DHC")
for i in range(1,len(lend)):
    print("Valor en el grupo "+str(i)+" es: ", lend[i])
#print(lend)
#plt.legend(lend)
plt.yticks(yticks,cluster_labels+1)
plt.ylabel("Cluster")
plt.xlabel("Silhouette Coefficients DHC")
plt.show()
print("El promedio o Average silhouette witdh DHC: ", round(silhouette_avg,2))

#Validacion Externa
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import normalized_mutual_info_score
lista_grupos = list(df_group)
lista_labelsD = list(labelsD)
print()
print("Validación Externa")
ariD = adjusted_rand_score(lista_grupos, lista_labelsD)
#print(lista_especies)
#print(lista_labels)
#print(lista_labelsD)
print()
print("ARI DHC",ariD)
print()
amiD = adjusted_mutual_info_score(lista_grupos, lista_labelsD)
print("AMI DHC",amiD)
print()
nmiD = normalized_mutual_info_score(lista_grupos, lista_labelsD)
print("NMI DHC",nmiD)





