"""SIP Proxy Server"""

# !/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import socket
import sys
import time
import json
import hashlib
import random
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from uaclient import log


class Proxy_XmlHandler(ContentHandler):

    """XML Management class."""

    def __init__(self):

        """Initializer method."""

        self.tags = {}

    def startElement(self, name, attrs):

        """Handler for .xml data.

        Extracts and stores data from a given xml
        """

        info_xml = {}
        atributes_1 = ['name', 'ip', 'puerto']
        atributes_2 = ['path', 'passwdpath']
        atributes_3 = ['path']
        tags = {'server': atributes_1, 'database': atributes_2,
                'log': atributes_3}
        if name in tags:
            for atribute in tags[name]:
                if name == 'server' and atribute == 'ip':
                    if attrs.get(atribute, "127.0.0.1") != "":
                        info_xml[atribute] = attrs.get(atribute, "127.0.0.1")
                else:
                    if attrs.get(atribute, "") != "":
                        info_xml[atribute] = attrs.get(atribute, "")
                self.tags[name] = info_xml

    def get_tags(self):

        """Information retriever method."""

        return self.tags


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    """SIP server class."""

    data_list = []
    nonce = []
    resend_ad = {}
    resend_port = {}
    d = {}
    p = {}

    def handle(self):

        """Handler for SIP management.

        Functionality:
        Receive and manage REGISTER petitions
        Keeping client information
        Ban clients with overtimed expiration
        """
        # Registro de clientes almacenados en el fichero .json
        self.json2registered()
        # Comprobación de la caducidad de los registros
        self.expiration()
        # Procesado de mensaje
        lines = self.rfile.read()
        slices = lines.decode('utf-8').split()
        method = slices[0]

        print('Received:')
        print(lines.decode('utf-8'))

        # Manejo de los distintos mensajes (REGISTER, INVITE, BYE, ACK)
        if method == 'REGISTER' and len(slices) >= 6:
            # Registro por segunda vez

            # Escribiendo en el log
            to_write = 'Received from ' + self.client_address[0] + ':' + \
                slices[1][-4:] + ': ' + \
                lines.decode('utf-8').replace('\r\n', ' ')
            log(config_data, to_write)

            authorization = slices[5]

            # Comprobar contraseña
            f = open(config_data['database']['passwdpath'], 'r')

            for line in f.readlines():
                if slices[1][4:-5] == line.split()[0][:-5]:

                    passwd = line.split()[0][-4:]
                    # Obtener el hash
                    authenticate = hashlib.sha1()
                    authenticate.update(bytes(passwd, 'utf-8'))
                    authenticate.update(bytes(self.nonce[0], 'utf-8'))
                    authenticate = authenticate.hexdigest()

                    if authenticate == slices[7][10:-1]:
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        # Escribiendo en el log
                        to_write = 'Sent to ' + self.client_address[0] + \
                            ':' + slices[1][-4:] + ': ' + 'SIP/2.0 200 OK '
                        log(config_data, to_write)
                        # Registro del cliente
                        slices = lines.decode('utf-8').split()
                        t = int(slices[4].split('/')[0])
                        date = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.gmtime(time.time()))
                        gm = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.gmtime(time.time()+t))
                        client = [slices[1][4:-5],
                                  {"address": self.client_address[0],
                                   "port":slices[1][-4:], "expires": gm,
                                   "register_date": date}]
                        # Si Expires=0, dar de baja al clliente
                        if slices[0] == 'REGISTER':
                            empty = True
                            reg = True
                            for usr in self.data_list:
                                empty = False
                                if usr[0] == client[0]:
                                    if slices[4].split('/')[0] == '0':
                                        exp = client[1]["expires"]
                                        date = client[1]["register_date"]
                                        usr[1]["expires"] = exp
                                        usr[1]["register_date"] = date
                                        self.data_list.remove(client)
                                        print('Time for client ' + client[0] +
                                              ' intentionally expired. ' +
                                              'Removed.')
                                        reg = False
                                    else:
                                        print('Client ' + client[0] +
                                              ' already registered. Updated.')
                                        exp = client[1]["expires"]
                                        date = client[1]["register_date"]
                                        usr[1]["expires"] = exp
                                        usr[1]["register_date"] = date
                                        reg = False
                            if empty or reg:
                                if slices[4].split('/')[0] != '0':
                                    self.data_list.append(client)
                                print('(^)Client successfully registered')
                        self.register2json()
                    else:
                        # Respuesta para contraseña incorrecta
                        print('Inorrect password for user: ' + slices[1][4:-5])
                        self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                        # Escribiendo en el log
                        to_write = 'Sent to ' + self.client_address[0] + \
                            ':' + slices[1][-4:] + ': ' + \
                            'SIP/2.0 400 Bad Request '
                        log(config_data, to_write)
                    self.nonce.clear()
        elif method == 'REGISTER' and len(slices) < 6:
            # Registro por primera vez. Se requiere autorización
            # Escribiendo en el log
            to_write = 'Received from ' + self.client_address[0] + ':' + \
                slices[1][-4:] + ': ' + \
                lines.decode('utf-8').replace('\r\n', ' ')
            log(config_data, to_write)
            self.nonce.append(str(random.randint(00000000000000000000,
                                                 99999999999999999999)))
            self.wfile.write(bytes(('SIP/2.0 401 Unauthorized\r\n' +
                                    'WWW-Authenticate: Digest nonce="' +
                                    self.nonce[0] + '"\r\n\r\n'), 'utf-8'))
            # Escribiendo en el log
            to_write = 'Sent to ' + self.client_address[0] + ':' + \
                slices[1][-4:] + ': ' + 'SIP/2.0 401 Unauthorized ' + \
                'WWW-Authenticate: Digest nonce="' + self.nonce[0] + '"  '
            log(config_data, to_write)

            print('(^)Not successfully registered, authentication required')
            print()

        elif method == 'INVITE':
            # Comprobar que el que hace la petición está registrado
            registered = False
            for client in self.data_list:
                if client[0] == slices[6][2:]:
                    self.d[client[0]] = client[1]["address"]
                    self.p[client[0]] = client[1]["port"]
                    # Escribiendo en el log
                    to_write = 'Received from ' + self.d[client[0]] + ':' + \
                        self.p[client[0]] + ': ' + \
                        lines.decode('utf-8').replace('\r\n', ' ')
                    log(config_data, to_write)
                    registered = True
            if not registered:
                # Escribiendo en el log
                to_write = 'Error: INVITE attempt from ' + \
                    self.client_address[0] + ':' + \
                    str(self.client_address[1]) + ' without previous REGISTER'
                log(config_data, to_write)
                print(to_write)
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                # Escribiendo en el log
                to_write = 'Sent to ' + self.client_address[0] + ': ' + \
                    str(self.client_address[1]) + ': SIP/2.0 400 Bad Request  '
                log(config_data, to_write)
                self.d.clear()
                self.p.clear()

            else:
                # Comprobar que al que le hacen el invite esta registrado

                resend = False
                for client in self.data_list:
                    if client[0] == slices[1][4:]:
                        resend = True
                        # Reenvío de INVITE, recepción y reenvío de respuesta
                        with socket.socket(socket.AF_INET,
                                           socket.SOCK_DGRAM) as my_socket:
                            add = client[1]["address"]
                            my_socket.connect((add, int(client[1]["port"])))
                            self.resend_ad[client[0]] = add
                            self.resend_port[client[0]] = client[1]["port"]
                            my_socket.send(bytes(lines.decode('utf-8'),
                                                 'utf-8'))
                            print()
                            print("Resending: (" + client[1]["address"] +
                                  "," + client[1]["port"] + ")")
                            print(lines.decode('utf-8'))
                            # Escribiendo en el log
                            to_write = 'Sent to ' + self.resend_ad[client[0]]
                            to_write += ':' + self.resend_port[client[0]] + \
                                ': ' + \
                                lines.decode('utf-8').replace('\r\n', ' ')
                            log(config_data, to_write)
                            # Recibir el 200 OK con el sdp
                            response = my_socket.recv(1024).decode('utf-8')
                            print('Received --', response)
                            # Escribiendo en el log
                            to_write = 'Received from ' + \
                                self.resend_ad[client[0]] + ':' + \
                                self.resend_port[client[0]] + ': ' + \
                                response.replace('\r\n', ' ')
                            log(config_data, to_write)
                            # Reenviar al cliente
                            self.wfile.write(bytes(response, 'utf-8'))
                            # Escribiendo en el log
                            to_write = 'Sent to ' + self.d[slices[6][2:]] + \
                                ':' + self.p[slices[6][2:]] + ': ' + \
                                response.replace('\r\n', ' ')
                            log(config_data, to_write)
                if not resend:
                    print('User ' + slices[1][4:] + ' Not Found. Resending (' +
                          self.d[slices[6][2:]] + ':' + self.p[slices[6][2:]] +
                          '): SIP/2.0 404 User Not Found\r\n\r\n')
                    self.wfile.write(b"SIP/2.0 404 User Not Found\r\n\r\n")
                    # Escribiendo en el log
                    to_write = 'Error: INVITE attempt from ' + \
                        self.d[slices[6][2:]] + ':' + self.p[slices[6][2:]] + \
                        ': User Not Found'
                    log(config_data, to_write)
                    self.d.clear()
                    self.p.clear()

        elif method == 'ACK':
            # Respuesta al INVITE
            ack_slices = lines.decode('utf-8').split()
            for client in self.data_list:
                if client[0] != slices[1][4:]:
                    d = client[1]["address"]
                    p = client[1]["port"]
            # Escribiendo en el log
            to_write = 'Received from ' + d + ':' + p + \
                ': ' + lines.decode('utf-8').replace('\r\n', ' ')
            log(config_data, to_write)
            # Reenviando ACK
            print("Resending: (" + self.resend_ad[slices[1][4:]] + "," +
                  self.resend_port[slices[1][4:]] + ")")
            print(lines.decode('utf-8'))
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
                add = self.resend_ad[slices[1][4:]]
                port = self.resend_port[slices[1][4:]]
                my_socket.connect((add, int(port)))
                my_socket.send(bytes(lines.decode('utf-8'), 'utf-8'))

            # Escribiendo en el log
            to_write = 'Sent to ' + add + ':' + port + \
                ': ' + lines.decode('utf-8').replace('\r\n', ' ')
            log(config_data, to_write)
            self.resend_ad.clear()
            self.resend_port.clear()
            self.d.clear()
            self.p.clear()

        elif method == 'BYE':
            # Escribiendo en el log
            to_write = 'Received from ' + self.client_address[0] + ':' + \
                str(self.client_address[1]) + ': ' + \
                lines.decode('utf-8').replace('\r\n', ' ')
            log(config_data, to_write)

            dest = slices[1][4:]
            resend = False
            # Reenviando BYE
            for client in self.data_list:
                if client[0] == dest:
                    resend = True
                    with socket.socket(socket.AF_INET,
                                       socket.SOCK_DGRAM) as my_socket:
                        add = client[1]["address"]
                        port = client[1]["port"]
                        my_socket.connect((add, int(port)))
                        my_socket.send(bytes(lines.decode('utf-8'), 'utf-8'))
                        print()
                        print("Resending: (" + add + "," + port + ")")
                        print(lines.decode('utf-8'))
                        # Escribiendo en el log
                        to_write = 'Sent to ' + add + ':' + port + \
                            ': ' + lines.decode('utf-8').replace('\r\n', ' ')
                        log(config_data, to_write)
                        # Recibir el 200 OK
                        response = my_socket.recv(1024).decode('utf-8')
                        print('Received --', response)
                        # Escribiendo en el log
                        to_write = 'Received from ' + add + ':' + port + \
                            ': ' + response.replace('\r\n', ' ')
                        log(config_data, to_write)
                        # Reenviar al cliente
                        self.wfile.write(bytes(response, 'utf-8'))
                        print("Resending (" + self.client_address[0] + "," +
                              str(self.client_address[1]) + "): " + response)
                        # Escribiendo en el log
                        to_write = 'Sent to ' + self.client_address[0] + \
                            ':' + str(self.client_address[1]) + \
                            ': ' + response.replace('\r\n', ' ')
                        log(config_data, to_write)

            if not resend:
                self.wfile.write(b"SIP/2.0 404 User Not Found\r\n\r\n")
                # Escribiendo en el log
                to_write = 'Error: BYE attempt from ' + \
                    self.client_address[0] + ':' + \
                    str(self.client_address[1]) + ': User Not Found'
                log(config_data, to_write)
                to_write = 'Sent to ' + self.client_address[0] + ':' + \
                    str(self.client_address[1]) + \
                    ': SIP/2.0 404 User Not Found '
                log(config_data, to_write)
        elif method not in ['REGISTER', 'INVITE', 'ACK', 'BYE']:
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            print('Method ' + method + ' not allowed.')
            # Escribiendo en el log
            to_write = 'Error: Method ' + method + ' not allowed.'
            log(config_data, to_write)
            to_write = 'Sent: SIP/2.0 405 Method Not Allowed '
            log(config_data, to_write)

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
    try:
        CONFIG = sys.argv[1]
    except (IndexError, ValueError):
        sys.exit("Usage:\n python3 proxy_registrar.py config")

    parser = make_parser()
    cHandler = Proxy_XmlHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(CONFIG))

    config_data = cHandler.get_tags()
    # Escribiendo en el log
    log(config_data, 'Starting...')

    serv = socketserver.UDPServer(('', int(config_data['server']['puerto'])),
                                  SIPRegisterHandler)
    print("Server Sheldon_Proxy listening at port " +
          config_data['server']['puerto'] + " ...")
    print()
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        # Escribiendo en el log
        log(config_data, 'Finishing.')
        print("Ending proxy.")
