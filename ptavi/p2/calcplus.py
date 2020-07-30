#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import calcoohija

if __name__ == "__main__":

    calculator = calcoohija.DaughterCalculator()
    file = open(sys.argv[1], 'r')

    lines = file.readlines()
    operatorDict = {'suma': calculator.plus, 'resta': calculator.minus,
                    'multiplica': calculator.mult, 'divide': calculator.div}

    for line in lines:
        elements = line.split(',')

        operation = elements[0]
        elements = elements[1:]
        elements[-1] = elements[-1][:-1]

        result = int(elements[0])
        elements = elements[1:]

        for element in elements:
            if operation == 'divide' and int(element) == 0:
                sys.exit('Division by zero is not allowed')
            else:
                try:
                    result = operatorDict[operation](result, int(element))
                except KeyError:
                    sys.exit('[ERROR] Allowed Operations: suma, resta,'
                             ' multiplica o divide.')

        print(result)
