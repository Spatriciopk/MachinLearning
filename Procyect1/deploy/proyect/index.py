
from turtle import distance
from flask import Flask, flash, request, redirect, url_for, send_from_directory,render_template
import pandas as pd
import re
import nltk 
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
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.datasets as dt
from sklearn.manifold import MDS
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc
from werkzeug.utils import secure_filename
import os
n = stopwords.words("english")
stemmer = PorterStemmer()

app = Flask(__name__)
UPLOAD_FOLDER = 'static/archivo' 
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
archivo_selec = False
url_archivo ="static/archivo/server_interno.csv"
delimitador=""

@app.route('/')
def principal():
    return render_template("index.php")


@app.route('/Shedule.php')
def schedule():
    return render_template("Schedule.php")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    global delimitador
    global archivo_selec
    if(request.method=="POST"):
        f = request.files["upfile"]
        archivo_selec = True
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],"server_interno.csv"))
        return render_template("/Schedule.php")

@app.route("/quitar", methods=["GET", "POST"])
def quitar():
    global delimitador
    global archivo_selec
    if(request.method=="POST"):
        delimitador = ""
        archivo_selec = False
        return render_template("/Schedule.php")


def minusculas(lista):
    tit = []
    for token in lista:
        tit.append(token.lower())
    return tit

def caracter_especiales(lista):
    tit = []
    for token in lista:
        tit.append(re.sub('[^A-Za-z0-9]+', ' ', token))
    return tit

def importacion_columnas(columna):
    url = "https://raw.githubusercontent.com/Freddy8-C/Proyecto_MachineLearning/master/csv/Proyecto.csv"
    data = pd.read_csv(url)
    columna = data[columna].tolist()
    return columna

def import_data_set():
    global url_archivo
    url = url_archivo
    data = pd.read_csv(url)
    return data

def importacion_columnas_serve(data,columna):
    columna = data[columna].tolist()
    return columna

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


@app.route('/Papers')
def documentos():
    global archivo_selec
    if( archivo_selec == False):
        titulos = importacion_columnas("Titles")
        keyword = importacion_columnas("Keywords")
        abstract = importacion_columnas("Abstract")
        return render_template("Papers.php",abstract = abstract, tam=len(abstract),keyword=keyword,titulos=titulos)
    else:
        data = import_data_set()
        titulos = importacion_columnas_serve(data,"Titles")
        keyword = importacion_columnas_serve(data,"Keywords")
        abstract = importacion_columnas_serve(data,"Abstract")
        return render_template("Papers.php",abstract = abstract, tam=len(abstract),keyword=keyword,titulos=titulos)

@app.route('/Dendrogram')
def dendograma():
    global archivo_selec
    if( archivo_selec == False):
        titulos = importacion_columnas("Titles")
        keyword = importacion_columnas("Keywords")
        abstract = importacion_columnas("Abstract")
        titulos = caracter_especiales(titulos)
        titulos = minusculas(titulos)

        keyword = caracter_especiales(keyword)
        keyword = minusculas(keyword)

        abstract = caracter_especiales(abstract)
        abstract = minusculas(abstract)

        #Tokenizacion

        titulos = tokenizacion(titulos)
        keyword = tokenizacion(keyword)
        abstract = tokenizacion(abstract)

        #Stopwords
        titulos = eliminar_stop_words(titulos)
        keyword = eliminar_stop_words(keyword)
        abstract = eliminar_stop_words(abstract)

        #Stemming

        titulos = stemming(titulos)
        keyword = stemming(keyword)
        abstract = stemming(abstract)

        
        matriz = np.zeros((len(titulos), len(titulos)))
        matriz_keywords = np.zeros((len(keyword), len(keyword)))
        llenar_identidad(matriz)
        llenar_identidad(matriz_keywords)
        jacard(titulos,matriz)
        jacard(keyword,matriz_keywords)
        ##### Matriz de distancias de titulos ########
        #print(matriz)
            
        ##### Matriz de distancias de keywords ########")
        #print(matriz_keywords)
        vocabulario = []
        generar_vocabulario(abstract, vocabulario)
        matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
        frecuencia = []
        lista_wtf = [] 
        lista_df = []   
        lista_idf = []  
        lista_tf_idf = []  
        lista_modulo = [] 
        lista_normal = []   
        lista_abstract_final =[]   
        frecuencias(vocabulario, abstract,frecuencia)
        #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
        llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
        llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
        #########Term Frecuency#############")
        #print(matriz_df_idf)
        print()
        #########Weight Document Frecuency#############")
        matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
        calcular_wtf(frecuencia, lista_wtf)
        llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
        llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
        #print(matriz_wtf)
        print()
        #########Document Frecuency#############")
        matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
        calcular_df(lista_wtf, lista_df,vocabulario)
        llenar_palabras_documentos(vocabulario, abstract, matriz_df)
        llenar_matriz2(lista_df,matriz_df,"DF: ")
        #print(matriz_df)
        print()
        #########Inverse Document Frecuency#############")
        matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
        calcular_idf(lista_df, abstract, lista_idf)
        llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
        llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
        #print(matriz_idf)
        print()
        ######### TF - IDF#############")
        matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
        calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
        lista_tf_idf =redondear(lista_tf_idf)
        llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
        llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
        #print(matriz_tf_idf)
        print()
        ######### Matriz de distancias abstract #############")
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
        #print(matriz_distancia_abs)
        print()
        ##### Matriz de distancias de titulos con 20%  ########")
        matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
        #print(matriz_tit_20)
        print()
        ##### Matriz de distancias de keywords con 30%  ########")
        matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
        #print(matriz_key_30)
        print()
        ######### Matriz de distancias abstract 50%#############")
        matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
        #print(matriz_abs_50)
        print()
        matriz_aux = np.add(matriz_tit_20,matriz_key_30)
        matriz_resultante = np.add(matriz_aux,matriz_abs_50)
        return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))
    else:
        data = import_data_set()
        titulos = importacion_columnas_serve(data,"Titles")
        keyword = importacion_columnas_serve(data,"Keywords")
        abstract = importacion_columnas_serve(data,"Abstract")
        titulos = caracter_especiales(titulos)
        titulos = minusculas(titulos)

        keyword = caracter_especiales(keyword)
        keyword = minusculas(keyword)

        abstract = caracter_especiales(abstract)
        abstract = minusculas(abstract)

        #Tokenizacion

        titulos = tokenizacion(titulos)
        keyword = tokenizacion(keyword)
        abstract = tokenizacion(abstract)

        #Stopwords
        titulos = eliminar_stop_words(titulos)
        keyword = eliminar_stop_words(keyword)
        abstract = eliminar_stop_words(abstract)

        #Stemming

        titulos = stemming(titulos)
        keyword = stemming(keyword)
        abstract = stemming(abstract)

        
        matriz = np.zeros((len(titulos), len(titulos)))
        matriz_keywords = np.zeros((len(keyword), len(keyword)))
        llenar_identidad(matriz)
        llenar_identidad(matriz_keywords)
        jacard(titulos,matriz)
        jacard(keyword,matriz_keywords)
        ##### Matriz de distancias de titulos ########
        #print(matriz)
            
        ##### Matriz de distancias de keywords ########")
        #print(matriz_keywords)
        vocabulario = []
        generar_vocabulario(abstract, vocabulario)
        matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
        frecuencia = []
        lista_wtf = [] 
        lista_df = []   
        lista_idf = []  
        lista_tf_idf = []  
        lista_modulo = [] 
        lista_normal = []   
        lista_abstract_final =[]   
        frecuencias(vocabulario, abstract,frecuencia)
        #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
        llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
        llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
        #########Term Frecuency#############")
        #print(matriz_df_idf)
        print()
        #########Weight Document Frecuency#############")
        matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
        calcular_wtf(frecuencia, lista_wtf)
        llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
        llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
        #print(matriz_wtf)
        print()
        #########Document Frecuency#############")
        matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
        calcular_df(lista_wtf, lista_df,vocabulario)
        llenar_palabras_documentos(vocabulario, abstract, matriz_df)
        llenar_matriz2(lista_df,matriz_df,"DF: ")
        #print(matriz_df)
        print()
        #########Inverse Document Frecuency#############")
        matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
        calcular_idf(lista_df, abstract, lista_idf)
        llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
        llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
        #print(matriz_idf)
        print()
        ######### TF - IDF#############")
        matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
        calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
        lista_tf_idf =redondear(lista_tf_idf)
        llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
        llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
        #print(matriz_tf_idf)
        print()
        ######### Matriz de distancias abstract #############")
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
        #print(matriz_distancia_abs)
        print()
        ##### Matriz de distancias de titulos con 20%  ########")
        matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
        #print(matriz_tit_20)
        print()
        ##### Matriz de distancias de keywords con 30%  ########")
        matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
        #print(matriz_key_30)
        print()
        ######### Matriz de distancias abstract 50%#############")
        matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
        #print(matriz_abs_50)
        print()
        matriz_aux = np.add(matriz_tit_20,matriz_key_30)
        matriz_resultante = np.add(matriz_aux,matriz_abs_50)
        return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))

@app.route('/doc/<num>')
def tot_documentos(num):
    global archivo_selec
    if(archivo_selec == False):
        titulos = importacion_columnas("Titles")
        keyword = importacion_columnas("Keywords")
        abstract = importacion_columnas("Abstract")
        
        if( num == '1'):
                abstract = importacion_columnas("Abstract")
                titulos = importacion_columnas("Titles")
                keyword = importacion_columnas("Keywords")
                
        elif( num == '2'):
                abstract = abstract[0:48]
                titulos = titulos[0:48]
                keyword = keyword[0:48]
                
        elif( num == '3'):
                abstract = abstract[48:96]
                titulos = titulos[48:96]
                keyword = keyword[48:96]
                
        elif( num == '4'):
                abstract = abstract[96:144]
                titulos = titulos[96:144]
                keyword = keyword[96:144]
                
        elif( num == '5'):
                abstract = abstract[144:192]
                titulos = titulos[144:192]
                keyword = keyword[144:192]
                
        return render_template("Papers.php",abstract = abstract, tam=len(abstract),keyword=keyword,titulos=titulos)
    else:
        data = import_data_set()
        titulos = importacion_columnas_serve(data,"Titles")
        keyword = importacion_columnas_serve(data,"Keywords")
        abstract = importacion_columnas_serve(data,"Abstract")
        if( num == '1'):
                titulos = importacion_columnas_serve(data,"Titles")
                keyword = importacion_columnas_serve(data,"Keywords")
                abstract = importacion_columnas_serve(data,"Abstract")    
        return render_template("Papers.php",abstract = abstract, tam=len(abstract),keyword=keyword,titulos=titulos)
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

def generar_vocabulario(documentos,vocabulario):
    for documento in documentos:
        for palabra in documento:
            if(palabra not in vocabulario):
                vocabulario.append(palabra)

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

def llenardoc (tam,vector):
    for i in range(0,tam):
        vector.append("Doc "+str(i))

@app.route('/dendo/<num>')
def tot_dendogr(num):
    global archivo_selec
    if(archivo_selec == False):
        titulos = importacion_columnas("Titles")
        keyword = importacion_columnas("Keywords")
        abstract = importacion_columnas("Abstract")
        if(num == '1'):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            #print(type(matriz_resultante))
            columa =[]
            llenardoc(len(matriz_resultante),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_resultante, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))
        


                    
        elif(num == '2'):
            abstract = abstract[0:48]
            titulos = titulos[0:48]
            keyword = keyword[0:48]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            columa =[]
            llenardoc(len(matriz_resultante),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_resultante, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))
        


                    
        elif(num == '3'):
            titulos = titulos[0:48]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            #Tokenizacion

            titulos = tokenizacion(titulos)
        

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            

            #Stemming

            titulos = stemming(titulos)
        

        
            matriz = np.zeros((len(titulos), len(titulos)))
            
            llenar_identidad(matriz)
        
            jacard(titulos,matriz)
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            columa =[]
            llenardoc(len(matriz_tit_20),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_tit_20, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_tit_20, tam =len(matriz_tit_20))

        
        elif(num == '4'):
            keyword = keyword[0:48]
            
            #Normalizacion

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            #Tokenizacion

            keyword = tokenizacion(keyword)
        

            #Stopwords
            keyword = eliminar_stop_words(keyword)
            

            #Stemming

            keyword = stemming(keyword)
        

        
            matriz = np.zeros((len(keyword), len(keyword)))
            
            llenar_identidad(matriz)
        
            jacard(keyword,matriz)
            matriz_key_30 = np.around(np.matrix(matriz*0.30),2)
            columa =[]
            llenardoc(len(matriz_key_30),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_key_30, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_key_30, tam =len(matriz_key_30))
                    
        elif(num == '5'):
            abstract = abstract[0:48]
            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            abstract = tokenizacion(abstract)
        

            #Stopwords
            abstract = eliminar_stop_words(abstract)
            

            #Stemming

            abstract = stemming(abstract)

            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            columa =[]
            llenardoc(len(matriz_abs_50),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_abs_50, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_abs_50,2), tam =len(matriz_abs_50))
                    
                ######Nueva seccion
        elif(num == '6'):
            abstract = abstract[48:96]
            titulos = titulos[48:96]
            keyword = keyword[48:96]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            columa =[]
            llenardoc(len(matriz_resultante),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_resultante, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))
        


                
        elif(num == '7'):
            titulos = titulos[48:96]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            #Tokenizacion

            titulos = tokenizacion(titulos)
        

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            

            #Stemming

            titulos = stemming(titulos)
        

        
            matriz = np.zeros((len(titulos), len(titulos)))
            
            llenar_identidad(matriz)
        
            jacard(titulos,matriz)
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            columa =[]
            llenardoc(len(matriz_tit_20),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_tit_20, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_tit_20, tam =len(matriz_tit_20))

                    
        elif(num == '8'):
            keyword = keyword[48:96]
            
            #Normalizacion

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            #Tokenizacion

            keyword = tokenizacion(keyword)
        

            #Stopwords
            keyword = eliminar_stop_words(keyword)
            

            #Stemming

            keyword = stemming(keyword)
        

        
            matriz = np.zeros((len(keyword), len(keyword)))
            
            llenar_identidad(matriz)
        
            jacard(keyword,matriz)
            matriz_key_30 = np.around(np.matrix(matriz*0.30),2)
            columa =[]
            llenardoc(len(matriz_key_30),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_key_30, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_key_30, tam =len(matriz_key_30))
        elif(num == '9'):
            abstract = abstract[48:96]
            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            abstract = tokenizacion(abstract)
        

            #Stopwords
            abstract = eliminar_stop_words(abstract)
            

            #Stemming

            abstract = stemming(abstract)

            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            columa =[]
            llenardoc(len(matriz_abs_50),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_abs_50, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_abs_50,2), tam =len(matriz_abs_50))
                
                ######Nueva seccion
        elif(num == '10'):
            abstract = abstract[96:144]
            titulos = titulos[96:144]
            keyword = keyword[96:144]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            columa =[]
            llenardoc(len(matriz_resultante),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_resultante, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))
        


                    
        elif(num == '11'):
            titulos = titulos[96:144]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            #Tokenizacion

            titulos = tokenizacion(titulos)
        

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            

            #Stemming

            titulos = stemming(titulos)
        

        
            matriz = np.zeros((len(titulos), len(titulos)))
            
            llenar_identidad(matriz)
        
            jacard(titulos,matriz)
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            columa =[]
            llenardoc(len(matriz_tit_20),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_tit_20, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_tit_20, tam =len(matriz_tit_20))

                
        elif(num == '12'):
            keyword = keyword[96:144]
            
            #Normalizacion

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            #Tokenizacion

            keyword = tokenizacion(keyword)
        

            #Stopwords
            keyword = eliminar_stop_words(keyword)
            

            #Stemming

            keyword = stemming(keyword)
        

        
            matriz = np.zeros((len(keyword), len(keyword)))
            
            llenar_identidad(matriz)
        
            jacard(keyword,matriz)
            matriz_key_30 = np.around(np.matrix(matriz*0.30),2)
            columa =[]
            llenardoc(len(matriz_key_30),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_key_30, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_key_30, tam =len(matriz_key_30))
            
        elif(num == '13'):
            abstract = abstract[96:144]
            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            abstract = tokenizacion(abstract)
        

            #Stopwords
            abstract = eliminar_stop_words(abstract)
            

            #Stemming

            abstract = stemming(abstract)

            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            columa =[]
            llenardoc(len(matriz_abs_50),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_abs_50, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_abs_50,2), tam =len(matriz_abs_50))
                    
                ######Nueva seccion
        elif(num == '14'):
            abstract = abstract[144:192]
            titulos = titulos[144:192]
            keyword = keyword[144:192]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            columa =[]
            llenardoc(len(matriz_resultante),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_resultante, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))
        


                
        elif(num == '15'):
            titulos = titulos[144:192]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            #Tokenizacion

            titulos = tokenizacion(titulos)
        

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            

            #Stemming

            titulos = stemming(titulos)
        

        
            matriz = np.zeros((len(titulos), len(titulos)))
            
            llenar_identidad(matriz)
        
            jacard(titulos,matriz)
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            columa =[]
            llenardoc(len(matriz_tit_20),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_tit_20, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_tit_20, tam =len(matriz_tit_20))

                    
        elif(num == '16'):
            keyword = keyword[144:192]
            #Normalizacion

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            #Tokenizacion

            keyword = tokenizacion(keyword)
        

            #Stopwords
            keyword = eliminar_stop_words(keyword)
            

            #Stemming

            keyword = stemming(keyword)
        

        
            matriz = np.zeros((len(keyword), len(keyword)))
            
            llenar_identidad(matriz)
        
            jacard(keyword,matriz)
            matriz_key_30 = np.around(np.matrix(matriz*0.30),2)
            columa =[]
            llenardoc(len(matriz_key_30),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_key_30, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            return render_template("Dendrogram.php",matriz_keywords = matriz_key_30, tam =len(matriz_key_30))

                    
        elif(num == '17'):
            abstract = abstract[144:192]
            
            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            abstract = tokenizacion(abstract)
        

            #Stopwords
            abstract = eliminar_stop_words(abstract)
            

            #Stemming

            abstract = stemming(abstract)

            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            columa =[]
            llenardoc(len(matriz_abs_50),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_abs_50, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_abs_50,2), tam =len(matriz_abs_50))
    else:
            data = import_data_set()
            titulos = importacion_columnas_serve(data,"Titles")
            keyword = importacion_columnas_serve(data,"Keywords")
            abstract = importacion_columnas_serve(data,"Abstract")
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
            #print(matriz_resultante)
            #print(type(matriz_resultante))
            columa =[]
            llenardoc(len(matriz_resultante),columa)
            plt.figure(figsize=(6.4,4.8))
            df = pd.DataFrame(matriz_resultante, columns = columa )
            mapa1 =sns.heatmap(df,cmap="Blues",vmin=0, vmax=1)
            figure = mapa1.get_figure()
            figure.savefig('static/img/mapa1.png')
            
            return render_template("Dendrogram.php",matriz_keywords = np.around(matriz_resultante,2), tam =len(matriz_resultante))

    
@app.route('/MDS', methods=["GET", "POST"])
def grafo():
    return render_template("MDS.php")

@app.route('/MDS/<num>', methods=["GET", "POST"])
def tot_grafo(num):
    global archivo_selec
    if(archivo_selec == False):
        abstract = importacion_columnas("Abstract")
        titulos = importacion_columnas("Titles")
        keyword = importacion_columnas("Keywords")
        tipo_distancia="euclidean"
        if request.method == 'POST':
                tipo_distancia = request.form['carlist']
        if(num == '1'):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            mds = MDS(metric=True, dissimilarity=tipo_distancia, random_state=0)
            X_transform = mds.fit_transform(matriz_resultante)
        
        
            # Get the embeddings
            fig, ax = plt.subplots()
            ax.scatter(X_transform[:,0], X_transform[:,1],color="green")
            for i in range(len(X_transform)):
                ax.annotate(str(i+1),(X_transform[i][0],X_transform[i][1]))
            ax.set_title("Metric MDS General "+tipo_distancia)
            figure = ax.get_figure()
            figure.savefig('static/img/mds.png')
        elif(num =='2'):
            abstract = abstract[0:48]
            titulos = titulos[0:48]
            keyword = keyword[0:48]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            mds = MDS(metric=True, dissimilarity=tipo_distancia, random_state=0)
            X_transform = mds.fit_transform(matriz_resultante)
        
            # Get the embeddings
            fig, ax = plt.subplots()
            ax.scatter(X_transform[:,0], X_transform[:,1],color="green")
            for i in range(len(X_transform)):
                ax.annotate(str(i+1),(X_transform[i][0],X_transform[i][1]))
            ax.set_title("Metric MDS Social Sciences "+tipo_distancia)
            figure = ax.get_figure()
            figure.savefig('static/img/mds.png')

        elif(num=='3'):
            abstract = abstract[48:96]
            titulos = titulos[48:96]
            keyword = keyword[48:96]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            mds = MDS(metric=True, dissimilarity=tipo_distancia, random_state=0)
            X_transform = mds.fit_transform(matriz_resultante)
        
            # Get the embeddings
            fig, ax = plt.subplots()
            ax.scatter(X_transform[:,0], X_transform[:,1],color="green")
            for i in range(len(X_transform)):
                ax.annotate(str(i+1),(X_transform[i][0],X_transform[i][1]))
            ax.set_title("Metric MDS Computing "+tipo_distancia)
            figure = ax.get_figure()
            figure.savefig('static/img/mds.png')

        elif(num=='4'):
            abstract = abstract[96:144]
            titulos = titulos[96:144]
            keyword = keyword[96:144]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            mds = MDS(metric=True, dissimilarity=tipo_distancia, random_state=0)
            X_transform = mds.fit_transform(matriz_resultante)
        
            # Get the embeddings
            fig, ax = plt.subplots()
            ax.scatter(X_transform[:,0], X_transform[:,1],color="green")
            for i in range(len(X_transform)):
                ax.annotate(str(i+1),(X_transform[i][0],X_transform[i][1]))
            ax.set_title("Metric MDS Medicine "+tipo_distancia)
            figure = ax.get_figure()
            figure.savefig('static/img/mds.png')
        elif(num=='5'):
            abstract = abstract[144:192]
            titulos = titulos[144:192]
            keyword = keyword[144:192]
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

        
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
            
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            mds = MDS(metric=True, dissimilarity=tipo_distancia, random_state=0)
            X_transform = mds.fit_transform(matriz_resultante)
        
            # Get the embeddings
            fig, ax = plt.subplots()
            ax.scatter(X_transform[:,0], X_transform[:,1],color="green")
            for i in range(len(X_transform)):
                ax.annotate(str(i+1),(X_transform[i][0],X_transform[i][1]))
            ax.set_title("Metric MDS Exact Sciencies "+tipo_distancia)
            figure = ax.get_figure()
            figure.savefig('static/img/mds.png')
        
        return render_template("MDS.php")
    else:
        data = import_data_set()
        titulos = importacion_columnas_serve(data,"Titles")
        keyword = importacion_columnas_serve(data,"Keywords")
        abstract = importacion_columnas_serve(data,"Abstract")
        tipo_distancia="euclidean"
        if request.method == 'POST':
                tipo_distancia = request.form['carlist']
        if(num == '1'):
            titulos = importacion_columnas_serve(data,"Titles")
            keyword = importacion_columnas_serve(data,"Keywords")
            abstract = importacion_columnas_serve(data,"Abstract")
            #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

            #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

            #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

            #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
            #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
            #########Term Frecuency#############")
            #print(matriz_df_idf)
            print()
            #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
            #print(matriz_wtf)
            print()
            #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
            #print(matriz_df)
            print()
            #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
            #print(matriz_idf)
            print()
            ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
            #print(matriz_tf_idf)
            print()
            ######### Matriz de distancias abstract #############")
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
            #print(matriz_distancia_abs)
            print()
            ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
            #print(matriz_tit_20)
            print()
            ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
            #print(matriz_key_30)
            print()
            ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
            #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
            mds = MDS(metric=True, dissimilarity=tipo_distancia, random_state=0)
            X_transform = mds.fit_transform(matriz_resultante)
        
        
            # Get the embeddings
            fig, ax = plt.subplots()
            ax.scatter(X_transform[:,0], X_transform[:,1],color="green")
            for i in range(len(X_transform)):
                ax.annotate(str(i+1),(X_transform[i][0],X_transform[i][1]))
            ax.set_title("Metric MDS General "+tipo_distancia)
            figure = ax.get_figure()
            figure.savefig('static/img/mds.png')
        return render_template("MDS.php")

@app.route('/Cluster/', methods=["GET", "POST"])
def cluster():
        global archivo_selec
        if(archivo_selec==False):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
            print(altura)

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)
        else:
            data = import_data_set()
            titulos = importacion_columnas_serve(data,"Titles")
            keyword = importacion_columnas_serve(data,"Keywords")
            abstract = importacion_columnas_serve(data,"Abstract")
            
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
            print(altura)

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)




@app.route('/Cluster/<num>', methods=["GET", "POST"])
def cluster2(num):
    global archivo_selec
    if(archivo_selec==False):
        if(num =="1"):
        
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
            print(altura)

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)

        if(num=="2"):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            abstract = abstract[0:48]
            titulos = titulos[0:48]
            keyword = keyword[0:48]
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
            print(altura)

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)
        if(num=="3"):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            abstract = abstract[48:96]
            titulos = titulos[48:96]
            keyword = keyword[48:96]
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
            print(altura)

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)
        if(num=="4"):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            abstract = abstract[96:144]
            titulos = titulos[96:144]
            keyword = keyword[96:144]
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
            print(altura)

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)
        if(num=="5"):
            abstract = importacion_columnas("Abstract")
            titulos = importacion_columnas("Titles")
            keyword = importacion_columnas("Keywords")
            abstract = abstract[144:192]
            titulos = titulos[144:192]
            keyword = keyword[144:192]
                #Normalizacion

            titulos = caracter_especiales(titulos)
            titulos = minusculas(titulos)

            keyword = caracter_especiales(keyword)
            keyword = minusculas(keyword)

            abstract = caracter_especiales(abstract)
            abstract = minusculas(abstract)

                #Tokenizacion

            titulos = tokenizacion(titulos)
            keyword = tokenizacion(keyword)
            abstract = tokenizacion(abstract)

                #Stopwords
            titulos = eliminar_stop_words(titulos)
            keyword = eliminar_stop_words(keyword)
            abstract = eliminar_stop_words(abstract)

                #Stemming

            titulos = stemming(titulos)
            keyword = stemming(keyword)
            abstract = stemming(abstract)

            
            matriz = np.zeros((len(titulos), len(titulos)))
            matriz_keywords = np.zeros((len(keyword), len(keyword)))
            llenar_identidad(matriz)
            llenar_identidad(matriz_keywords)
            jacard(titulos,matriz)
            jacard(keyword,matriz_keywords)
            ##### Matriz de distancias de titulos ########
            #print(matriz)
                
            ##### Matriz de distancias de keywords ########")
            #print(matriz_keywords)
            vocabulario = []
            generar_vocabulario(abstract, vocabulario)
            matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            frecuencia = []
            lista_wtf = [] 
            lista_df = []   
            lista_idf = []  
            lista_tf_idf = []  
            lista_modulo = [] 
            lista_normal = []   
            lista_abstract_final =[]   
            frecuencias(vocabulario, abstract,frecuencia)
                #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
            llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
            llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                #########Term Frecuency#############")
                #print(matriz_df_idf)
            print()
                #########Weight Document Frecuency#############")
            matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_wtf(frecuencia, lista_wtf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
            llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                #print(matriz_wtf)
            print()
                #########Document Frecuency#############")
            matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_df(lista_wtf, lista_df,vocabulario)
            llenar_palabras_documentos(vocabulario, abstract, matriz_df)
            llenar_matriz2(lista_df,matriz_df,"DF: ")
                #print(matriz_df)
            print()
                #########Inverse Document Frecuency#############")
            matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
            calcular_idf(lista_df, abstract, lista_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
            llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                #print(matriz_idf)
            print()
                ######### TF - IDF#############")
            matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
            calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
            lista_tf_idf =redondear(lista_tf_idf)
            llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
            llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                #print(matriz_tf_idf)
            print()
                ######### Matriz de distancias abstract #############")
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
                #print(matriz_distancia_abs)
            print()
                ##### Matriz de distancias de titulos con 20%  ########")
            matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                #print(matriz_tit_20)
            print()
                ##### Matriz de distancias de keywords con 30%  ########")
            matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                #print(matriz_key_30)
            print()
                ######### Matriz de distancias abstract 50%#############")
            matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                #print(matriz_abs_50)
            print()
            matriz_aux = np.add(matriz_tit_20,matriz_key_30)
            matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                #print(matriz_resultante)
                #print(type(matriz_resultante))
            columa =[]
            altura=2
            if request.method == 'POST':
                altura = request.form['name']
            altura = float(altura)
        

            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
            linked = linkage(matriz_resultante,'complete')
            dend = dendrogram(linked,
                                    orientation='top',
                                    distance_sort='descending',
                                show_leaf_counts=True,
                                    color_threshold=altura

                                    )

            ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
            titulos_aux = importacion_columnas("Titles")
            aux = []
            for i in range (len(dend['leaves'])):
                aux.append(titulos_aux[int(dend['leaves'][i])-1])
                figure = fig.get_figure()
            figure.savefig('static/img/cluster.png')
            resultantList = []
        
            for element in dend['leaves_color_list']:
                if element not in resultantList:
                    resultantList.append(element)

        
            return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)
    else:
        if(num =="1"):
                data = import_data_set()
                titulos = importacion_columnas_serve(data,"Titles")
                keyword = importacion_columnas_serve(data,"Keywords")
                abstract = importacion_columnas_serve(data,"Abstract")

                
                    #Normalizacion

                titulos = caracter_especiales(titulos)
                titulos = minusculas(titulos)

                keyword = caracter_especiales(keyword)
                keyword = minusculas(keyword)

                abstract = caracter_especiales(abstract)
                abstract = minusculas(abstract)

                    #Tokenizacion

                titulos = tokenizacion(titulos)
                keyword = tokenizacion(keyword)
                abstract = tokenizacion(abstract)

                    #Stopwords
                titulos = eliminar_stop_words(titulos)
                keyword = eliminar_stop_words(keyword)
                abstract = eliminar_stop_words(abstract)

                    #Stemming

                titulos = stemming(titulos)
                keyword = stemming(keyword)
                abstract = stemming(abstract)

                
                matriz = np.zeros((len(titulos), len(titulos)))
                matriz_keywords = np.zeros((len(keyword), len(keyword)))
                llenar_identidad(matriz)
                llenar_identidad(matriz_keywords)
                jacard(titulos,matriz)
                jacard(keyword,matriz_keywords)
                ##### Matriz de distancias de titulos ########
                #print(matriz)
                    
                ##### Matriz de distancias de keywords ########")
                #print(matriz_keywords)
                vocabulario = []
                generar_vocabulario(abstract, vocabulario)
                matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
                frecuencia = []
                lista_wtf = [] 
                lista_df = []   
                lista_idf = []  
                lista_tf_idf = []  
                lista_modulo = [] 
                lista_normal = []   
                lista_abstract_final =[]   
                frecuencias(vocabulario, abstract,frecuencia)
                    #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
                llenar_palabras_documentos(vocabulario, abstract, matriz_df_idf)
                llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
                    #########Term Frecuency#############")
                    #print(matriz_df_idf)
                print()
                    #########Weight Document Frecuency#############")
                matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
                calcular_wtf(frecuencia, lista_wtf)
                llenar_palabras_documentos(vocabulario, abstract, matriz_wtf)
                llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
                    #print(matriz_wtf)
                print()
                    #########Document Frecuency#############")
                matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
                calcular_df(lista_wtf, lista_df,vocabulario)
                llenar_palabras_documentos(vocabulario, abstract, matriz_df)
                llenar_matriz2(lista_df,matriz_df,"DF: ")
                    #print(matriz_df)
                print()
                    #########Inverse Document Frecuency#############")
                matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
                calcular_idf(lista_df, abstract, lista_idf)
                llenar_palabras_documentos(vocabulario, abstract, matriz_idf)
                llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
                    #print(matriz_idf)
                print()
                    ######### TF - IDF#############")
                matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstract)+1),dtype=object)
                calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
                lista_tf_idf =redondear(lista_tf_idf)
                llenar_palabras_documentos(vocabulario, abstract, matriz_tf_idf)
                llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
                    #print(matriz_tf_idf)
                print()
                    ######### Matriz de distancias abstract #############")
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
                    #print(matriz_distancia_abs)
                print()
                    ##### Matriz de distancias de titulos con 20%  ########")
                matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
                    #print(matriz_tit_20)
                print()
                    ##### Matriz de distancias de keywords con 30%  ########")
                matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
                    #print(matriz_key_30)
                print()
                    ######### Matriz de distancias abstract 50%#############")
                matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
                    #print(matriz_abs_50)
                print()
                matriz_aux = np.add(matriz_tit_20,matriz_key_30)
                matriz_resultante = np.add(matriz_aux,matriz_abs_50)
                    #print("######### Matriz de distancias con la sumatoria de titulos,keywords y abstrac#############")
                    #print(matriz_resultante)
                    #print(type(matriz_resultante))
                columa =[]
                altura=2
                if request.method == 'POST':
                    altura = request.form['name']
                altura = float(altura)
                print(altura)

                fig, ax = plt.subplots(1, 1, figsize=(8, 4))
                linked = linkage(matriz_resultante,'complete')
                dend = dendrogram(linked,
                                        orientation='top',
                                        distance_sort='descending',
                                    show_leaf_counts=True,
                                        color_threshold=altura

                                        )

                ax.axhline(y=altura, c = 'black', linestyle='--', label='altura corte')
                titulos_aux = importacion_columnas("Titles")
                aux = []
                for i in range (len(dend['leaves'])):
                    aux.append(titulos_aux[int(dend['leaves'][i])-1])
                    figure = fig.get_figure()
                figure.savefig('static/img/cluster.png')
                resultantList = []
            
                for element in dend['leaves_color_list']:
                    if element not in resultantList:
                        resultantList.append(element)

            
                return render_template("Cluster.php",tam=len(aux),data=aux,clust=dend['leaves_color_list'],tam2=len(resultantList),resultantList=resultantList)


#if __name__ == '__main__':
#    app.run()
