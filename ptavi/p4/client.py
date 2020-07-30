""" UDP Client """

# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket

try:

    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    line = ' '.join(sys.argv[3:5])
    expires_value = sys.argv[5]

except:

    sys.exit("Usage: client.py <'ip'> <'port'> <'udp_data'> <'sip_address'>"
             " <'expires_value'>")

exp_line = 'Expires: ' + expires_value + '\r\n\r\n'
slices = line.split(' ')
line = slices[0].upper() + " sip:" + slices[1] + ' SIP/2.0\r\n' + exp_line

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

    my_socket.connect((SERVER, PORT))
    print("Sending:", line)
    my_socket.send(bytes(line, 'utf-8'))
    data = my_socket.recv(1024)
    print(data.decode('utf-8'))

print("Socket finished.")
