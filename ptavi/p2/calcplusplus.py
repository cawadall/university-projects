#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import calcoohija
import csv

if __name__ == "__main__":

    calculator = calcoohija.DaughterCalculator()
    with open(sys.argv[1]) as fichero:
        for row in csv.reader(fichero):
            operation = row[0]
            result = int(row[1])
            row = row[2:]
            for element in row:
                if operation == "suma":
                    result = calculator.plus(result, int(element))
                elif operation == "resta":
                    result = calculator.minus(result, int(element))
                elif operation == "multiplica":
                    result = calculator.mult(result, int(element))
                elif operation == "divide":
                    if int(element) == 0:
                        sys.exit('Division by zero is not allowed')
                    else:
                        result = calculator.div(result, int(element))
                else:
                    sys.exit('[ERROR] Allowed Operations: suma, resta,'
                             ' multiplica o divide.')

            print(result)
