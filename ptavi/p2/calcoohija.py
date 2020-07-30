#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

class Calculator():
    ''' Calculator Class with common computing methods '''

    def plus(self, op1, op2):

        return op1 + op2

    def minus(self, op1, op2):

        return op1 - op2


class DaughterCalculator(Calculator): # inheritance
    ''' Extension of Calculator Class including some other methods '''    

    def mult(self, op1, op2):
        return op1 * op2

    def div(self, op1, op2):
        if op2 == 0:
            sys.exit('Division by zero is not allowed')
        else:
            return op1 / op2

if __name__ == "__main__":

    calculator = DaughterCalculator()
    try:
        operando1 = int(sys.argv[1])
        operando2 = int(sys.argv[3])
    except ValueError:
        sys.exit("Error: Non numerical parameters")
    except IndexError:
        sys.exit("Error: Try:\n python3 calcoohija.py <'op1'> " +
                 "<'operación'> <'op2'> ")

    operador = sys.argv[2]

    operatorDict = {'suma': calculator.plus, 'resta': calculator.minus,
                    'multiplica': calculator.mult, 'divide': calculator.div}

    if operador == 'divide' and operando2 == 0:
        sys.exit('Division by zero is not allowed')
    else:
        result = operatorDict[operador](operando1, operando2)

    print(result)
