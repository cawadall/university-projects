#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math

if __name__ == "__main__":

    try:
        LAeq = float(sys.argv[1])
        LCeq = float(sys.argv[2])
        LAIeq = float(sys.argv[3])
        LAeq_ruido = float(sys.argv[4])
        LCeq_ruido = float(sys.argv[5])
        LAIeq_ruido = float(sys.argv[6])
        tipo_actividad = sys.argv[7]

        if (tipo_actividad != 'infraestructura_viaria' \
        and tipo_actividad != 'actividad' \
        and tipo_actividad != 'actividad_colindante'):

            sys.exit("Error: No es un tipo de actividad válido, prueba con: "
                     "infraestructura_viaria, actividad o actividad_colindante") 
                   
    except ValueError:

        sys.exit("Error: Algún parámetro no es del tipo correcto, prueba "
                  "ejecutando: \n'python3 ' + <'Nombre fichero'> + <'LAeq'> + "
                  "<'LCeq'> + <'LAIeq'> + <'LAeq rudio de fondo'> + "
                  "<'LCeq rudio de fondo'> + <'LAIeq rudio de fondo'> + "
                  "<'Tipo de actividad: infraestructura_viaria, actividad o "
                  "actividad_colindante'")  
    
    # COMENZAMOS CON LA CORRECIÓN POR RUIDO DE FONDO    
    
    LAeq_corr = 10 * math.log(10**(LAeq/10) - 10**(LAeq_ruido/10))
    LCeq_corr = 10 * math.log(10**(LCeq/10) - 10**(LCeq_ruido/10))
    LAIeq_corr = 10 * math.log(10**(LAIeq/10) - 10**(LAIeq_ruido/10))
    
    # CALCULAMOS LOS ÍNDICES DE CORRECIÓN AL NIVEL DE EVALUACIÓN
    
    # Empezamos por la penalización por bajas frecuencias:
    Lf = LCeq_corr - LAeq_corr
    if Lf <= 10:
        Kf = 0
    elif Lf > 15:
        Kf = 6
    else:
        Kf = 3
        
    # Continuamos con la penalización por impulsividad:		
    Li = LAIeq_corr - LAeq_corr
    if Li <= 10:
        Ki = 0
    elif Li > 15:
        Ki = 6
    else:
        Ki = 3
        
    Kt = 0
    
    # Por último, calculamos el NIVEL DE EVALUACIÓN
    Lkeq = LAeq_corr + Ki + Kf + Kt
    Lkeq = round(Lkeq)  # Para obtener un valor representativo, redondeamos.
    print("\n| -------------------- | ----- |")
    print("| Nivel de Evaluación  |", Lkeq, "   |")
    print("| -------------------- | ----- |\n")
    
    # COMPARAMOS CON LA TABLA RESPECTIVA SEGÚN LA CLASE DE ACTIVIDAD
    
    if tipo_actividad == 'infraestructura_viaria':
        if Lkeq <= 60 + 5:
            print("SÍ SE CUMPLE LA NORMATIVA ESTABLECIDA POR EL RD1367")
        else: 
            print("NO SE CUMPLE LA NORMATIVA ESTABLECIDA POR EL RD1367")            
    elif tipo_actividad == 'actividad':
        if Lkeq <= 55 + 5:
            print("SÍ SE CUMPLE LA NORMATIVA ESTABLECIDA POR EL RD1367")
        else: 
            print("NO SE CUMPLE LA NORMATIVA ESTABLECIDA POR EL RD1367") 
    else:
        if Lkeq <= 40 + 5:
            print("SÍ SE CUMPLE LA NORMATIVA ESTABLECIDA POR EL RD1367")
        else: 
            print("NO SE CUMPLE LA NORMATIVA ESTABLECIDA POR EL RD1367")
