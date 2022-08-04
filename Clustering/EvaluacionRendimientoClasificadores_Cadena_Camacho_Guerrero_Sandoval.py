#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 19:01:29 2022

@author: spatricio
"""


import numpy as np
matrix_confusion = np.matrix([[944,0,5,3,0,12,14,1,1,0],
                             [0,1100,4,4,1,0,2,2,22,0],
                             [20,18,873,22,18,0,20,18,40,3],
                             [10,2,29,888,2,34,2,18,19,6],
                             [1,1,5,0,893,1,20,3,6,52],
                             [21,6,3,47,11,721,26,9,41,7],
                             [20,2,12,1,18,15,883,0,7,0],
                             [5,20,27,2,8,1,0,935,4,26],
                             [7,19,11,24,11,46,29,14,792,21],
                             [10,2,2,12,53,14,1,35,14,866]])
#matrix_confusion = np.matrix( [[130,74,2,6]
#                    ,[96,99,6,16],
#                    [3,4,207,4]
#                    ,[6,12,4,177]])
lista_diagonal = matrix_confusion.diagonal()
print("MATRIZ DE CONFUSION")
print(matrix_confusion)


print("######### Accuracy ############")
def calcular_accuracy(matrix_confusion):
    global lista_diagonal
    return round(lista_diagonal.sum()/matrix_confusion.sum(),3)

print(calcular_accuracy(matrix_confusion))


print("######### Precision ############")

#print(matrix_confusion.diagonal())  #obtener valores de la diagonal
#print(matrix_confusion[:, 0].sum()) # suma la columna
#print(matrix_confusion[3].sum()) #suma la fila
def calcular_precision (matrix_confusion):
   lista_precision = []
   global lista_diagonal
   for i in range(len(matrix_confusion)):
       lista_precision.append(round(lista_diagonal[0,i]/matrix_confusion[:, i].sum(),3))
   return lista_precision


lista_precision =  calcular_precision(matrix_confusion)
print("[C1      C2    C3     C4      C5     C6    C7    C8    C9      C10]")
print(lista_precision)

print("######### Recalll ############")

def calcular_recall(matrix_confusion):
    lista_recall=[]
    global lista_diagonal
    for i in range(len(matrix_confusion)):
        lista_recall.append(round(lista_diagonal[0,i]/matrix_confusion[i].sum(),3))
    return lista_recall
    

lista_recall =  calcular_recall(matrix_confusion)
print("[C1      C2    C3     C4      C5     C6    C7    C8    C9      C10]")
print(lista_recall)

print("######### F-Measuere #########")

def calcular_fmeasure(lista_precision,lista_recall):
    lista_fmesuare=[]
    for i in range(len(lista_precision)):
        lista_fmesuare.append(round((2*((lista_precision[i]*lista_recall[i])/(lista_precision[i]+lista_recall[i]))),3))
    return lista_fmesuare


lista_fmesuare= calcular_fmeasure(lista_precision,lista_recall)
print("[C1      C2    C3     C4      C5     C6    C7    C8    C9      C10]")
print(lista_fmesuare)






