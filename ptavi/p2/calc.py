#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

def plus(op1, op2):
    """ Function to sum the operands """

    return op1 + op2

def minus(op1, op2):
    """ Function to substract the operands """

    return op1 - op2

def mult(op1, op2):
    """ Function to multiply the operands """

    return op1 * op2

def div(op1, op2):
    """ Function to divide the operands """

    if op2 == 0:
        sys.exit('No se puede dividir por 0')
    else:
        return op1 / op2

if __name__ == "__main__":

    try:
        operando1 = int(sys.argv[1])
        operando2 = int(sys.argv[3])
    except ValueError:
        sys.exit("Error: Parámetros no numéricos")

    if sys.argv[2] == "suma":
        result = plus(operando1, operando2)
    elif sys.argv[2] == "resta":
        result = minus(operando1, operando2)
    elif sys.argv[2] == "multiplicacion":
        result = mult(operando1, operando2)
    elif sys.argv[2] == "division":
        result = div(operando1, operando2)
    else:
        sys.exit('Operación sólo puede ser sumar, restar, multiplicar'
                 ' o dividir.')

    print(result)
