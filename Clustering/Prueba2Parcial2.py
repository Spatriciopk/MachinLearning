#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 23:23:38 2022

@author: spatricio
"""

import numpy as np

matrixConfusion=np.matrix([[923,4,21,8,4,1],[5,972,2,0,0,0],
                           [26,2,892,30,13,8],[12,4,32,826,24,48],
                           [5,1,28,24,898,13],[7,2,28,111,18,801]])


#matrixConfusion = np.matrix( [[130,74,2,6]
#                    ,[96,99,6,16],
#                    [3,4,207,4]
#                    ,[6,12,4,177]])

lista_diagonal = matrixConfusion.diagonal()
print(matrixConfusion)
print("############")
print()
print("Determinar el tamaño del dataset")
print(matrixConfusion.sum())
print("############")
print("Indicar la cardinalidad de la clase predicha")
def cardinalidad (matrix_confusion):
   lista_precision = []
   global lista_diagonal
   for i in range(len(matrix_confusion)):
       lista_precision.append(matrix_confusion[:, i].sum())
   return lista_precision
print(cardinalidad(matrixConfusion))

print("############")
print("Determinar el TPR /recall o sensitividad")

def calcular_recall(matrixConfusion):
    lista_recall=[]
    global lista_diagonal
    for i in range(len(matrixConfusion)):
        lista_recall.append(round(lista_diagonal[0,i]/matrixConfusion[i].sum(),3))
    return lista_recall

lista_recall =  calcular_recall(matrixConfusion)
print(lista_recall)
print("############")
print("Determinar el False Negative Rate ")
print(1-np.array(lista_recall))
print("############")
print("Determinar el False Positive Rate ")

def false_positive_rate(matrixConfusion):
    lista_spe=[]
    lista=[]
    global lista_diagonal
    cont = 0
    for i in range(len(matrixConfusion)):
        lista.append(matrixConfusion[i].sum())
    for i in range(len(matrixConfusion)):
        superior = matrixConfusion[:, i].sum() - lista_diagonal[0,i]
        inferior = sum(lista) - lista[i]
        lista_spe.append(round(superior/inferior,3))
    return lista_spe

false_positive_r =false_positive_rate(matrixConfusion)
print(false_positive_rate(matrixConfusion))
print("############")
print("Determinar el recall para cada clase ")
lista_recall =  calcular_recall(matrixConfusion)
print(lista_recall)
print("############")
print("Determinar el accuracy ")
def calcular_accuracy(matrixConfusion):
    global lista_diagonal
    return round(lista_diagonal.sum()/matrixConfusion.sum(),3)

print(calcular_accuracy(matrixConfusion))
print("############")
print("Determinar la sensitividad ")
lista_recall =  calcular_recall(matrixConfusion)
print(lista_recall)
print("############")
print("Determinar el precision para cada clase")
def calcular_precision (matrix_confusion):
   lista_precision = []
   global lista_diagonal
   for i in range(len(matrix_confusion)):
       lista_precision.append(round(lista_diagonal[0,i]/matrix_confusion[:, i].sum(),3))
   return lista_precision

lista_precision =  calcular_precision(matrixConfusion)
print(lista_precision)
print(" Determinar la especificidad ")
print(1- np.array(false_positive_r))
print("############")
print("Determinar el número de fallos ")

print("Error por clase")
print( matrixConfusion.sum() - sum(lista_diagonal))

print("Error total")
print(matrixConfusion.sum() - lista_diagonal.sum())
