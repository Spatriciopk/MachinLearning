#Integrantes
#Cadena Patricio
#Camacho Freddy
#Guerrero Saskia


### pos = el modulo o la posicion que se selecciona de la cubeta
### k = k para encontrar la nueva posicion
### asignar metodo añadir el valor
### B es el tamaño

def modulo (datos,tabla_hash,B):
    for i in range(len(datos)):
        pos = datos[i]%B
        if( tabla_hash[pos] == None):
            asignar(tabla_hash, pos, datos, i)
        else:
            k = (datos[i] % (B -1)) +1 
            while (True):
                h = (pos + k) % B 
                if ( tabla_hash[h] == None ):
                    asignar(tabla_hash, h, datos, i)
                    break;
                else:
                    pos = h
        
def asignar (tabla_hash,pos,datos,indice):
    tabla_hash[pos] = datos[indice]
    
### Completa de NONE a nuestra tabla hash
### tabla_ash = donde vamos a guardar en cada cubeta 
### B = al tamaño, este debe ser igual o mayor al tamaño del vector
### datos = al vector
def auto_completar (tabla_hash,B,datos):
    if( B < len(datos)):
       
        return False
    else:
        for i in range(B):
            tabla_hash.append(None)
        return True


#datos = [2,324,90,12367,33,19]
datos = [51,14,3,7,18,30]
#datos = [23,14,9,6,30,12,18]
tabla_hash=[]
B = 11
print("Los datos son: ", datos);
print("########Tabla hash ###########") 
if(auto_completar(tabla_hash, B, datos)):
    modulo(datos, tabla_hash, B)
    print(tabla_hash)
else:
    print("El tamaño de B no es el correcto")

