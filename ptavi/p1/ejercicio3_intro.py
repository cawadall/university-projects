#!/usr/bin/python3        
# -*- coding: utf-8 -*-

file = open('/etc/passwd', 'r')

lines = file.readlines()
dic = {}

for line in lines:
    dic[line.split(':')[0]] = line.split(':')[-1][:-1]

# ///////////////////////////////////////////////////////////
# SOLUCION 1
try:
    print(dic["imaginario"]) 
except KeyError: 
    print("Clave inexistente")

try:
    print(dic["root"]) 
except KeyError: 
    print("Clave inexistente")

# ///////////////////////////////////////////////////////////
# SOLUCION 2    
users = ['imaginario', 'root']
for user in users:
    try:
        print(dic[user]) 
    except KeyError: 
        print("Clave inexistente")


   
    
