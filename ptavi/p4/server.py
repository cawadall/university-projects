""" UDP Server as SIP Registrar"""
# !/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    """Echo server class."""

    data_list = []

    def handle(self):

        """
        Handler for SIP management.

        Functionality:
            Receive and manage REGISTER petitions
            Keeps client information
            Ban clients with overtimed expiration
        """

        self.json2registered()
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        lines = self.rfile.read()
        self.expiration()
        slices = lines.decode('utf-8').split()
        t = int(slices[4].split('/')[0])
        gm = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()+t))
        client = [slices[1][4:],
                  {"address": self.client_address[0], "expires": gm}]
        if slices[4].split('/')[0] == '0':
            for usr in self.data_list:
                if usr[0] == slices[1][4:]:
                    self.data_list.remove(usr)
        if slices[0] == 'REGISTER':
            self.data_list.append(client)
            if slices[3][:-1] == 'Expires':
                if slices[4].split('/')[0] == '0':
                    self.data_list.remove(client)
        print(lines.decode('utf-8'))
        self.register2json()

    def register2json(self):

        """Copier of information in .json file."""

        json.dump(self.data_list, open('registered.json', 'w'), indent='\t')

    def json2registered(self):

        """Registrar of .json file information."""

        try:
            with open('registered.json') as clients_file:
                self.data_list = json.load(clients_file)
        except:
            self.register2json()

    def expiration(self):

        """Administrator of expiration time."""

        for usr in self.data_list:
            if usr[1]["expires"] <= time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.gmtime(time.time())):
                self.data_list.remove(usr)
                json.dump(self.data_list, open('registered.json', 'w'),
                          indent='\t')

if __name__ == "__main__":

    S_PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', S_PORT), SIPRegisterHandler)
    print("UDP Server Listenning...")
    print()
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finished Server.")
