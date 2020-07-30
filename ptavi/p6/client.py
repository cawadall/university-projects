#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""RTP Client"""

import socket
import sys
import socket

try:
    METHOD = sys.argv[1].upper()
    LOGIN = sys.argv[2].split('@')[0]
    chop = sys.argv[2].split('@')
    SERVER_IP = chop[1][:-5]
    SERVER_PORT = int(chop[1].split(':')[1])

except (IndexError, ValueError):
    sys.exit("Usage:\n python3 client.py <'method'> <'receiver@IP:SIPport'>")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

    try:
        my_socket.connect((SERVER_IP, SERVER_PORT))
    except socket.gaierror:
        sys.exit("[ERROR] Invalid IP:Port value")

    LINE = METHOD + " sip:" + LOGIN + '@' + SERVER_IP + ' SIP/2.0\r\n\r\n'
    if METHOD == 'INVITE':
        print("Sending: ", LINE)
        my_socket.send(bytes(LINE, 'utf-8'))
        data = my_socket.recv(1024)

        if data.decode('utf-8').split('\r\n')[4] == "SIP/2.0 200 OK" or \
           data.decode('utf-8') == "SIP/2.0 200 OK\r\n\r\n":
            print('Received --', data.decode('utf-8'))
            line = 'ACK' + " sip:" + LOGIN + '@' + SERVER_IP + \
                   ' SIP/2.0\r\n\r\n'
            my_socket.send(bytes(line, 'utf-8'))
        else:
            print("[ERROR] Message Not Recognized")

    elif METHOD == 'BYE':
        print("Sending: ", LINE)
        my_socket.send(bytes(LINE, 'utf-8'))
        data = my_socket.recv(1024)
    else:
        print('[ERROR] Method Not Allowed')

print("Finished socket...")
print("Bye.")
