#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" RTP User Agent Server"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):

    """ Server Class """

    def handle(self):

        """ 
        Handler for SIP and RTP management.

        Permanently listening until an INVITE is received. Once received, it
        sends an audio file to the SIP adress that made the request
        """

        data = self.rfile.read().decode('utf-8')
        slices = data.split()
        REQUEST = slices[0]
        if REQUEST == 'INVITE':
            print("Received: " + data)
            self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n" +
                             b"SIP/2.0 180 Ringing\r\n\r\n" +
                             b"SIP/2.0 200 OK\r\n\r\n")
        elif REQUEST == 'ACK':
            print("Received: " + data)
            aEjecutar = 'mp32rtp -i ' + self.client_address[0] + \
                        ' -p 23032 < ' + MP3_FILE
            print("Executing... ", aEjecutar)
            os.system(aEjecutar)
        elif REQUEST == 'BYE':
            print()
            print()
            print("Received: " + data)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif REQUEST not in ['INVITE', 'ACK', 'BYE']:
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
        else:
            self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")


if __name__ == "__main__":

    try:
        IP_PORT = sys.argv[1]
        S_PORT = int(sys.argv[2])
        MP3_FILE = sys.argv[3]
    except (IndexError, ValueError):
        sys.exit("Usage:\n python3 server.py <'IP'> <'port'> <'audio_file'>")

    serv = socketserver.UDPServer(('', S_PORT), EchoHandler)
    print("Listening...")
    print()
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Server Finished.")
