#Libreria Matematica
from cmath import sqrt
from typing import Iterable
from operator import mul

#Array
def array(lista):
    lista = list(Iterable)
    return lista

#Suma de Vectores
def sumaV(vector_1, vector_2):
    suma = [i+j for i,j in zip(vector_1,vector_2)]
    return suma

#Resta de Vectores
def restaV(vector_1, vector_2):
    diferencia = [i - j for i, j in zip(vector_1,vector_2)]
    return diferencia

#Multiplicar de Vectores
def multiV(vector_1, vector_2):
    multi = [i* j for i, j in zip(vector_1,vector_2)]
    return multi

#Producto escalar entre vectores
def productoV(vector_1, vector_2):
    total = sum([i*j for (i, j) in zip(vector_1, vector_2)])
    return total

#Normalizar un Vector para una lista
def normalizarV(vector_1):
    y = 0
    for x in vector_1:
        y += x**2
    y = y**0.5
    return [v/y for v in vector_1]

#Normalizar un Vector para una magnitud
def normalizarV2(vector_1):
    y = 0
    for x in vector_1:
        y += x**2
    return y**0.5

#Multiplicacion escalar de vectores
def multiplicacionV(vector_1, vector_2):
    total = [x*vector_1 for x in vector_2]
    return total
