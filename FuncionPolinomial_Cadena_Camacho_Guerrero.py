#Integrantes 
#Cadena Patricio
#Camacho Freddy
#Guerrero Saskia


def funcion_polinomial(vector_ascci,base,datos,resultado):
    for i in range(len(vector_ascci)):
        valor_numerico = 0
        exponente = len (vector_ascci[i]) -1
        for j in range (len (vector_ascci[i])):
            valor_numerico += (vector_ascci[i][j] * (base**exponente))
            exponente -= 1
        resultado[datos[i]] = valor_numerico

def minusculas(datos):
    for i in range (len(datos)):
        datos[i] = datos[i].lower()
    
def asignar_codigo_ascci(vector_ascci,datos,tamanio):
    auto_completar(vector_ascci, tamanio)
    for i in range(len(datos)):
        codigos =[]
        auto_completar(codigos,len(datos[i]))
        for j in range(len(datos[i])):
           codigos[j] = ord(datos[i][j])
        vector_ascci[i]=(codigos)

def auto_completar(vector_ascci,tamanio):
    for i in range(tamanio):
        vector_ascci.append(None)

def excepcion (a):
    if ( a >1):
        return True
    else:
        return False

datos = ["casa","hola","Teja","Barcelona","Tabla","ingeniero","Elementos","clave"]
vector_ascci = []
tamanio = len(datos)
base = 2
resultado ={}
print("######### Palabras ##########")
print(datos)
print("####### Elementos con su clave##########")
if(excepcion(base)):
    minusculas(datos)
    asignar_codigo_ascci(vector_ascci, datos,tamanio)
    funcion_polinomial(vector_ascci, base, datos, resultado)
    print(resultado)
else:
    print("La base debe ser mayor a 1")