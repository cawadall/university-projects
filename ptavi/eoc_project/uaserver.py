# !/usr/bin/python3
# -*- coding: utf-8 -*-
u"""UA Server for SIP Session"""

import sys
import socketserver
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import os
from uaclient import XmlHandler
from uaclient import log
from uaclient import cvlc
from uaclient import rtp
from threading import Thread


class SIP_ServerHandler(socketserver.DatagramRequestHandler):
    """SIP Server class."""

    dest_ip = []
    dest_port = []
    dest_rtpip = []
    dest_rtpport = []

    def handle(self):
        """Handler for SIP and RTP management.

        Permanently listening until an INVITE is received. Once received, it
        sends an audio file to the SIP adress that made the request
        """
        data = self.rfile.read().decode('utf-8')
        slices = data.split()
        REQUEST = slices[0]

        self.dest_ip.append(config_data['regproxy']['ip'])
        self.dest_port.append(config_data['regproxy']['puerto'])
        if REQUEST == 'INVITE':
            self.dest_rtpip.append(slices[7])
            self.dest_rtpport.append(slices[11])
            print("Received: " + data)
            # Escribiendo en el log
            to_write = 'Received from ' + self.dest_ip[0] + ':' + \
                self.dest_port[0] + ': ' + data.replace('\r\n', ' ')
            log(config_data, to_write)
            # Creando contenido SDP
            sdp = 'Content-Type: application/sdp\r\n\r\n' + 'v=0\r\n' + \
                'o=' + config_data['account']['username'] + ' ' + \
                config_data['uaserver']['ip'] + '\r\n' + \
                's=aprobar_ptavi\r\n' + 't=0\r\n' + 'm=audio ' + \
                config_data['rtpaudio']['puerto'] + ' RTP\r\n'
            line = "SIP/2.0 100 Trying\r\n\r\n" + \
                "SIP/2.0 180 Ringing\r\n\r\n" + "SIP/2.0 200 OK\r\n" + sdp
            self.wfile.write(bytes(line, 'utf-8'))
            print()
            print("Sending:")
            print(line)
            # Escribiendo en el log
            to_write = 'Sent to ' + self.dest_ip[0] + ':' + \
                self.dest_port[0] + ': ' + line.replace('\r\n', ' ')
            log(config_data, to_write)

        elif REQUEST == 'ACK':
            print("Received: " + data)
            # Escribiendo en el log
            to_write = 'Received from ' + self.dest_ip[0] + ':' + \
                self.dest_port[0] + ': ' + data.replace('\r\n', ' ')
            log(config_data, to_write)
            # Hilo para el envío RTP
            thread1 = Thread(target=rtp, args=(self.dest_rtpip[0],
                             self.dest_rtpport[0],
                             config_data['audio']['path'],))
            # Hilo para reproducir en VLC
            thread2 = Thread(target=cvlc, args=(self.dest_rtpip[0],
                             '12346',))
            thread1.start()
            time.sleep(0.2)
            thread2.start()

            # Escribiendo en el log
            to_write = 'Sent to ' + self.dest_rtpip[0] + ':' + \
                self.dest_rtpport[0] + ': ' + 'RTP CONTENT'
            log(config_data, to_write)

        elif REQUEST == 'BYE':
            # Paramos envío RTP y VLC
            os.system('killall mp32rtp 2> /dev/null')
            os.system('killall vlc 2> /dev/null')
            print()
            print("Received: " + data)
            # Escribiendo en el log
            to_write = 'Received from ' + self.dest_ip[0] + ':' + \
                self.dest_port[0] + ': ' + data.replace('\r\n', ' ')
            log(config_data, to_write)
            print()
            print("Sending:")
            print("SIP/2.0 200 OK\r\n\r\n")
            # Escribiendo en el log
            to_write = 'Sent to ' + self.dest_ip[0] + ':' + \
                self.dest_port[0] + ': ' + 'SIP/2.0 200 OK '
            log(config_data, to_write)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.dest_ip = []
            self.dest_port = []

        elif REQUEST not in ['INVITE', 'ACK', 'BYE']:
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            print('Method ' + REQUEST + 'not allowed.')
            # Escribiendo en el log
            to_write = 'Error: Method ' + REQUEST + 'not allowed.'
            log(config_data, to_write)
            to_write = 'Sent: SIP/2.0 405 Method Not Allowed '
            log(config_data, to_write)

        else:
            self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            print('Method ' + method + 'not allowed.')
            # Escribiendo en el log
            to_write = 'Error: Petition not recognised.'
            log(config_data, to_write)
            to_write = 'Sent: SIP/2.0 400 Bad Request '
            log(config_data, to_write)

if __name__ == "__main__":

    try:
        CONFIG = sys.argv[1]
    except (IndexError, ValueError):
        sys.exit("Usage: python3 uaserver.py config")

    parser = make_parser()
    cHandler = XmlHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(CONFIG))

    config_data = cHandler.get_tags()

    port = config_data['uaserver']['puerto']
    serv = socketserver.UDPServer(('', int(port)), SIP_ServerHandler)
    print("Listening...")
    print()
    # Escribiendo en el log
    log(config_data, 'Starting...')

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        log(config_data, 'Finishing.')
        print("Ending Server")
