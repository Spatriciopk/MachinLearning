#Integrantes 
#Cadena Patricio
#Camacho Freddy
#Guerrero Saskia
#Sandoval Jefferson


import re
from collections import defaultdict

def minusculas(coleccion):
    aux_coleccion =[]
    for documento in coleccion:
        aux_coleccion.append(documento.lower())
    return aux_coleccion

def remove_charac(coleccion):
    aux_coleccion =[]
    for documento in coleccion:    
        aux_coleccion.append(re.sub('[^A-Za-z0-9]+', ' ', documento))
    return aux_coleccion
        
def remove_space(coleccion):
    aux_coleccion =[]
    for documento in coleccion:    
        aux_coleccion.append(documento.split())
    return aux_coleccion

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
            


d1 = "To do is to be. To be is to do."
d2 = "To be or not to be. I am what I am."
d3 = "I think therefore I am. Do be do be do."
d4 = "Do do do, da da da. Let it be, let it be."
coleccion = []
palabra = []
full_index = []
diccionario = {}
coleccion.append(d1)
coleccion.append(d2)
coleccion.append(d3)
coleccion.append(d4)
print("COLECCION DE DOCUMENTOS ORIGINAL")
print(coleccion)
print("COLECCION DE DOCUMENTOS MODIFICADO")
coleccion = minusculas(coleccion)
coleccion = remove_charac(coleccion)

coleccion = remove_space(coleccion)


print("RESULTADO")
generar_vocabulario(coleccion, palabra)
generar_diccionario(palabra, diccionario)
full_inverted_index(coleccion, palabra, full_index,diccionario)
#print(diccionario)