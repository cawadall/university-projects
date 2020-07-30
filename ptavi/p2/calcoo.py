#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

class Calculator():
    ''' Calculator Class including common computing methods '''

    def plus(self, op1, op2):

        return op1 + op2

    def minus(self, op1, op2):

        return op1 - op2

if __name__ == "__main__":

    calculator = Calculator()
    try:
        operando1 = int(sys.argv[1])
        operando2 = int(sys.argv[3])
    except ValueError:
        sys.exit("Error: Parámetros no numéricos")
    except IndexError:
        sys.exit("Error: Prueba ejecutando:\n python3 calcoo.py <'op1'> " +
                 "<'operación'> <'op2'> ")

    if sys.argv[2] == "suma":
        result = calculator.plus(operando1, operando2)
    elif sys.argv[2] == "resta":
        result = calculator.minus(operando1, operando2)
    else:
        sys.exit('La operación sólo puede ser sumar o restar')

    print(result)
