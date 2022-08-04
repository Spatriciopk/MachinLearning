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
from collections import defaultdict

n = stopwords.words("english")
stemmer = PorterStemmer()

def importacion_columnas(columna):
    link ="https://raw.githubusercontent.com/stevenjss/-UCI-AAAI-13-Accepted-Papers---Papers/main/%5BUCI%5D%20AAAI-13%20Accepted%20Papers%20-%20Papers.csv"
    data = read_csv(link, sep=',')
    columna = data[columna].tolist()
    return columna

abstract = importacion_columnas("Abstract");
documento1 = abstract[0]
documento2 = abstract[1]
documento3 = abstract[2]
documento4 = abstract[3]
documento5 = abstract[4]
documento6 = abstract[5]
documentos = [documento1,documento2,documento3,documento4,documento5,documento6]

#Realizar el proceso NLP de normalización de los abstracts, 
#de los primeros seis documentos

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

#Normalizacion
abstract = caracter_especiales(documentos)
abstract = minusculas(abstract)

print("Normalización")
print(abstract)

#Realizar eliminación de stopwords, 
#stemming (algoritmo de Porter) y 
#tokenización de los abstracts, de los primeros seis documentos

#Tokenizacion
def tokenizacion(lista):
    tit = []
    aux = []
    for token in lista:
        aux.append(token.split())   
    tit = aux
    return tit
abstract = tokenizacion(abstract)

#Stopwords
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

abstract = eliminar_stop_words(abstract)


#Stemming
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

abstract = stemming(abstract)


print("Stopwords,stemming,tokenización")
print(abstract)


#Obtener el full inverted index, del literal anterior

palabra = []
full_index = []
diccionario = {}
def generar_vocabulario(coleccion,palabra):
    for documento in coleccion:
        for caracter in documento:
            if(caracter not in palabra):
                palabra.append(caracter)

def generar_diccionario (palabra,diccionario):
    for valor in palabra:
        diccionario[valor]= 0
def full_inverted_index(coleccion,palabra,full_index,diccionario):
    repeticion = 0
    sub_lista = []
    aux = defaultdict(list)
    lista = []
    vector_full = []
    vector_full_aux = []
    pos = 0
    pos_rep = 0
    for documento in coleccion:
       for vocabulario in palabra:
            repeticion = documento.count(vocabulario)
            if(repeticion !=0):
                sub_lista.append(repeticion)
       lista.append(sub_lista)
       sub_lista =[]
    for documento in coleccion:
        for index, item in enumerate(documento):
            aux[item].append(index+1)
        for vocabulario in palabra:
            if ( len(aux[vocabulario]) != 0):
                vector_full.append(vocabulario)
                vector_full.append(pos+1)
                vector_full.append(lista[pos][pos_rep])
                vector_full.append(aux[vocabulario])
                full_index.append(vector_full)
                pos_rep+=1
                vector_full = []
        pos_rep = 0
        aux = defaultdict(list)
        pos +=1
    for vocabulario in palabra:
        for varf in full_index:
            if ( varf[0]  == vocabulario):
                vector_full_aux.append(varf)
    acum=""
    for vocabulario in palabra:
        acum = "["
        for valor in vector_full_aux:
            
            if ( valor[0]  == vocabulario):
               acum = ""+acum + str(valor[1]) +"," + str(valor[2]) +"," +str(valor[3])+"],["
            
        diccionario[vocabulario] = acum[:len(acum)-2]
print("Full inverted index")
generar_vocabulario(abstract, palabra)
generar_diccionario(palabra, diccionario)
full_inverted_index(abstract, palabra, full_index,diccionario)
print(diccionario)

#Colocar en un tabla hash de tamaño 10, 
#los primeros 5 tokens del literal anterior. 
#Usar el sistema de codificación ASCII, con base a=3 y función polinomial
def asignar_codigo_ascci(vector_ascci,datos,tamanio):
    auto_completar(vector_ascci, tamanio)
    for i in range(len(datos)):
        codigos =[]
        auto_completar(codigos,len(datos[i]))
        for j in range(len(datos[i])):
           codigos[j] = ord(datos[i][j])
        vector_ascci[i]=(codigos)
           
def funcion_polinomial(vector_ascci,base,datos,resultado,codigos):
    for i in range(len(vector_ascci)):
        valor_numerico = 0
        exponente = len(vector_ascci[i]) -1
        for j in range (len(vector_ascci[i])):
            valor_numerico += (vector_ascci[i][j] * (base**exponente))
            exponente -= 1
        codigos.append(valor_numerico)
        resultado[datos[i]] = valor_numerico
def excepcion (a):
    if ( a >1):
        return True
    else:
        return False
def auto_completar(vector_ascci,tamanio):
    for i in range(tamanio):
        vector_ascci.append(None)

vector_ascci = []
base = 3
datos = palabra[0:5]
tamanio = len(datos)
resultado ={}
codigos = []
print("#######Polinomial#########")
if(excepcion(base)):
    asignar_codigo_ascci(vector_ascci, datos,tamanio)
    funcion_polinomial(vector_ascci, base, datos, resultado,codigos)
    print(resultado)
    print(codigos)
else:
    print("La base debe ser mayor a 1")

def auto_completar_has (tabla_hash,B,datos):
    if( B < len(datos)):
       
        return False
    else:
        for i in range(B):
            tabla_hash.append(None)
        return True
def modulo (datos,tabla_hash,B):
    for i in range(len(datos)):
        pos = datos[i]%B
        if( tabla_hash[pos] == None):
            asignar_has(tabla_hash, pos, datos, i)
        else:
            k = (datos[i] % (B -1)) +1 
            while (True):
                h = (pos + k) % B 
                if ( tabla_hash[h] == None ):
                    asignar_has(tabla_hash, h, datos, i)
                    break;
                else:
                    pos = h
        
def asignar_has (tabla_hash,pos,datos,indice):
    tabla_hash[pos] = datos[indice]
    
tabla_hash=[]
B = 10
print("########Tabla hash ###########") 
if(auto_completar_has(tabla_hash, B, codigos)):
    modulo(codigos, tabla_hash, B)
    print(tabla_hash)
else:
    print("El tamaño de B no es el correcto")


##Obtener la matriz de incidencia binaria,
# del literal 4, e indicar las dimensiones 
#de la matriz resultante

#palabra bolsa de palabras
#abstract aqui estan todos los documentos ya limpios

print("#########Matriz de incidencia binaria########")
#print(len(palabra))
#print(len(abstract)) #filas x columnas
matri=[]

def matriz_binaria(palabra,abstract,matri):
    for pl in palabra:
        aux = [0,0,0,0,0,0]
        cont = 0
        for documento in abstract: 
            for caracter in documento:
                if( pl == caracter):
                    aux[cont] = 1
                    break
            cont = cont +1
        matri.append(aux)  
                    
def imprimir_matriz_binari(matri,palabra,abstract):
    cont = 0
    #fila = 6
    print("Terminos  D1 D2 D3 D4 D5 D6")
    for i in range (len(palabra)):
        print(palabra[i],matri[cont])
        cont = cont + 1
    
matriz_binaria(palabra, abstract, matri)
imprimir_matriz_binari(matri, palabra, abstract)
print("Dimensiones ", len(palabra) ," x " , len(abstract))


##8.Obtener la matriz TF-IDF,
#del literal 4, e indicar las dimensiones
#de la matriz resultante (1 Pto.)
def frecuencias (vocabulario,abstract,frecuencia):
    lista_aux = []
  
    for lista in abstract:
        for palabra in vocabulario:
                lista_aux.append(lista.count(palabra))
        frecuencia.append(lista_aux)
        lista_aux = []
        
lista_wtf = [] 
lista_df = []   
lista_idf = []  
lista_tf_idf = []  
lista_modulo = [] 
lista_normal = []   
lista_abstract_final =[] 

frecuencia = []
frecuencias(palabra, abstract,frecuencia)
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

print("Matriz TF-IDF")
matriz_df_idf =  np.zeros((len(palabra)+1, len(abstract)+1),dtype=object)
llenar_palabras_documentos(palabra, abstract, matriz_df_idf)
llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")

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
        
matriz_wtf =  np.zeros((len(palabra)+1, len(abstract)+1),dtype=object)
calcular_wtf(frecuencia, lista_wtf)
llenar_palabras_documentos(palabra, abstract, matriz_wtf)
llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")

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
def llenar_matriz2 (frecuencia,matriz_df_idf,texto):
    for i in range(len(frecuencia)):
            matriz_df_idf[i+1][1] = texto +str(frecuencia[i])

matriz_df = np.zeros((len(palabra)+1, 2),dtype=object)
calcular_df(lista_wtf, lista_df,palabra)
llenar_palabras_documentos(palabra, abstract, matriz_df)
llenar_matriz2(lista_df,matriz_df,"DF: ")

def calcular_idf (lista_df,abstract,lista_idf):
    for dato in lista_df:
        #lista_idf.append(round(math.log(3/dato,10),2))
        lista_idf.append(round(math.log(len(abstract)/dato,10),2))


matriz_idf = np.zeros((len(palabra)+1, 2),dtype=object)
calcular_idf(lista_df, abstract, lista_idf)
llenar_palabras_documentos(palabra, abstract, matriz_idf)
llenar_matriz2(lista_idf,matriz_idf,"IDF: ")

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

matriz_tf_idf = np.zeros((len(palabra)+1, len(abstract)+1),dtype=object)
calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
lista_tf_idf =redondear(lista_tf_idf)
llenar_palabras_documentos(palabra, abstract, matriz_tf_idf)
llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
print(matriz_tf_idf)
print("Dimensiones ", len(palabra) ," x " , len(abstract))

###9.Mediante el coeficiente de Jaccard, 
#en función de los abstracts que han pasado
#todo el proceso de NLP, indique que tan similares 
#son los documentos D6 y D5 (1 Pto.)
print("Coeficiente de Jacard")
def llenar_identidad(matriz_jacar):
    for i in range(len(matriz_jacar[1])):
        for j in range(len(matriz_jacar[1])):
            if(i == j):
                matriz_jacar[i][j]=1
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
                
documento_jacar = [abstract[4],abstract[5]]

matriz_jacar = np.zeros((len(documento_jacar), len(documento_jacar)))
llenar_identidad(matriz_jacar)
jacard(documento_jacar,matriz_jacar)
#print(matriz_jacar)
print("    D5 \t   D6")
print(" D5 ",end="")
print(matriz_jacar[0])
print(" D6 ",end="")
print(matriz_jacar[1])