#!/usr/bin/python3
# -*- coding: utf-8 -*-

file = open('/etc/passwd', 'r')

# print(type(file.read()))    #para que me imprima el fichero y me diga el tipo
# print(file.readline())      #para leer la primera linea

# print(file.readlines())     #devuelve una lista con cada linea
# print(file.readlines()[0])  #primera linea de la lista

lines = file.readlines()

# PARA LEER NOMBRE DE USUARIO Y SHELL DE LA PRIMERA LINEA, SABIENDO QUE TIENE 
# 'X' CARACTERES:
#
first_line = lines[0] 
usr_name = first_line[:4]
shell = first_line[-10:-1])  # el último caracter es el salto de linea y 
                             # hay que eliminarlo
first_line = lines[0] 
print(first_line.find(':'))  # devuelve la posicion en la que esta ':'
position = first_line.rfind(':') #rfind lee desde el final hasta el principio

# PARA EL FICHERO ENTERO
for line in lines:
    print(line[:line.find(':')], '-->', line[line.rfind(':')+1:-1]) 

# ///////////////////////////////////////////////////////////////////
# OTRA FORMA DE SOLUCIONARLO
# ///////////////////////////////////////////////////////////////////

for line in lines
    elements = line.split(':')
    print(elements[0], '-->', elements[-1][:-1]) #me quedo el elemnto -1, y le 
                                     # quito el último caracter (salto de linea)
    
    







