#Cadena Patricio
#Camacho Freddy
#Guerrero Saskia
#Sandoval Jeferson

import re
import nltk  
import pandas as pd
import csv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import defaultdict

n = stopwords.words("english")
stemmer = PorterStemmer()

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

### Full inverted index #####
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


def importacion_limpia ():
    tit = []
    aux = []
    resultado = []
    with open('peliculas.csv', newline='') as File:  
        reader = csv.reader(File)
       
        for row in reader:
            tit.append(row)
    #for cadena in tit:
    for caracter in tit:
        aux = []
        for dg in caracter:
            if(dg != ""):
                aux.append(dg)
        resultado.append(aux)
    return resultado

coleccion = []
palabra = []
full_index = []
diccionario = {}


file = urlopen("https://whatsondisneyplus.com/")
html = file.read()
file.close()
soup = BeautifulSoup(html)
busca = soup.find_all("h3")

titulos = []
for titulo in busca:
    titulos.append(titulo.getText())
print("\n########################")
print("Vector de titulos a usar")
titulos = list(set(titulos))
titulos = titulos[15:25]
print(titulos)
#Normalizacion
print("\n########################")
print("Normalizacion")
titulos = caracter_especiales(titulos)
titulos = minusculas(titulos)
print(titulos)

#Tokenizacion
print("\n########################\n")
print("Tokenizacion")
titulos = tokenizacion(titulos)
print(titulos)

#Stopwords
titulos = eliminar_stop_words(titulos)
print("\n########################")
print("Eliminacion de stopwords")
print(titulos)

#Stemming
titulos = stemming(titulos)
print("\n########################")
print("Stemmings")
print(titulos)
dat = pd.DataFrame(titulos)
dat.to_csv('peliculas.csv', encoding='utf-8', index=False ,header=False)
titulos =importacion_limpia()
generar_vocabulario(titulos,palabra)
generar_diccionario(palabra, diccionario)
full_inverted_index(titulos, palabra, full_index,diccionario)
print("\n########################\n")
print("Full inverted Index")
print(diccionario)

