u"""UA Client for SIP Session"""

# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from threading import Thread
import hashlib
import os
import time

class XmlHandler(ContentHandler):

    """XML Management class."""

    def __init__(self):

        """Initializer method."""

        self.tags = {}

    def startElement(self, name, attrs):

        """Handler for .xml data.

        Extracts and stores data from a given xml
        """

        info_xml = {}
        atributes_1 = ['username', 'passwd']
        atributes_2 = ['ip', 'puerto']
        atributes_3 = ['puerto']
        atributes_4 = ['ip', 'puerto']
        atributes_5 = ['path']
        atributes_6 = ['path']
        tags = {'account': atributes_1, 'uaserver': atributes_2,
                'rtpaudio': atributes_3, 'regproxy': atributes_4,
                'log': atributes_5, 'audio': atributes_6}
        if name in tags:
            for atribute in tags[name]:
                if name == 'uaserver' and atribute == 'ip':
                    if attrs.get(atribute, "127.0.0.1") != "":
                        info_xml[atribute] = attrs.get(atribute, "127.0.0.1")
                else:
                    if attrs.get(atribute, "") != "":
                        info_xml[atribute] = attrs.get(atribute, "")
                self.tags[name] = info_xml

    def get_tags(self):

        """Information retriever method."""

        return self.tags

# Función para registrar lo sucedido en el .log
def log(config_data, text):

    """Event logging method."""

    with open(config_data['log']['path'], 'a') as f:
        hour = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))
        text = hour + ' ' + text + '\r\n'
        f.write(text)

def cvlc(ip, puerto):

    """Thread for cvlc playback."""

    cmdVLC = 'cvlc rtp://@' + ip + ':' + puerto + ' 2> /dev/null &'
    print("Executing...", cmdVLC)
    os.system(cmdVLC)

def rtp(ip, puerto, cancion):

    """Thread for rtp shipping."""

    aEjecutar = ('./mp32rtp -i ' + ip + ' -p ' +
                 puerto + ' < ' +
                 cancion)
    print("Executing...", aEjecutar)
    os.system(aEjecutar)
    print('Succesfully sent')

if __name__ == "__main__":

    try:
        CONFIG = sys.argv[1]
        METHOD = sys.argv[2].upper()
        if METHOD == 'REGISTER':
            OPTION = int(sys.argv[3])
        elif METHOD in ['INVITE', 'BYE']:
            OPTION = sys.argv[3]
        else:
            sys.exit("Invalid Method")
    except (IndexError, ValueError):
        sys.exit("Usage:\n python3 uaclient.py <'config'> <'method'> <'option'>")

    parser = make_parser()
    cHandler = XmlHandler()
    parser.setContentHandler(cHandler)

    try:
        parser.parse(open(CONFIG))
    except FileNotFoundError:
        sys.exit("[ERROR] No such file or directory: '" + CONFIG + "'")

    config_data = cHandler.get_tags()
    try:
        ip = config_data['regproxy']['ip']
        p = config_data['regproxy']['puerto']
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.connect((ip, int(p)))

            if METHOD == 'REGISTER':
                # Enviando...
                exp_line = 'Expires: ' + str(OPTION) + '\r\n\r\n'
                line = METHOD + " sip:" + \
                    config_data['account']['username'] + ':' + \
                    config_data['uaserver']['puerto'] + ' SIP/2.0\r\n'
                to_send = line + exp_line
                my_socket.send(bytes(to_send, 'utf-8'))
                print()
                print("Sending:")
                print(to_send)
                # Escribiendo en el log
                to_write = 'Sent to ' + ip + ':' + p + ': ' + \
                    to_send.replace('\r\n', ' ')
                log(config_data, to_write)
                # Recibiendo...
                data = my_socket.recv(1024)

                if data.decode('utf-8').split()[1] == '401':
                    print('Received --', data.decode('utf-8'))
                    # Escribiendo en el log
                    to_write = 'Received from ' + ip + ':' + p + ': ' + \
                        data.decode('utf-8').replace('\r\n', ' ')
                    log(config_data, to_write)

                    nonce = data.decode('utf-8').split()[5].split('"')[1]
                    print(nonce)
                    # Obtención del hash y autorización
                    response = hashlib.sha1()
                    passwd = config_data['account']['passwd']
                    response.update(bytes(passwd, 'utf-8'))
                    response.update(bytes(nonce, 'utf-8'))
                    response = response.hexdigest()

                    authorization = 'Authorization: Digest response="' + \
                        response + '"\r\n\r\n'
                    line += 'Expires: ' + str(OPTION) + '\r\n' + authorization
                    my_socket.send(bytes(line, 'utf-8'))
                    print()
                    print("Sending:")
                    print(line)
                    # Escribiendo en el log
                    to_write = 'Sent to ' + ip + ':' + p + ': ' + \
                        line.replace('\r\n', ' ')
                    log(config_data, to_write)

                    data = my_socket.recv(1024)
                    print('Received --', data.decode('utf-8'))
                    # Escribiendo en el log
                    to_write = 'Received from ' + ip + ':' + \
                        p + ': ' + data.decode('utf-8').replace('\r\n', ' ')
                    log(config_data, to_write)
                else:
                    print("Unrecognized message")

            elif METHOD == 'INVITE':
                name = config_data['account']['username']
                content_type_header = 'Content-Type: application/sdp\r\n\r\n'
                sip_body = 'v=0\r\n' + 'o=' + name + ' ' + \
                    config_data['uaserver']['ip'] + '\r\n' + \
                    's=aprobar_ptavi\r\n' + 't=0\r\n' + 'm=audio ' + \
                    config_data['rtpaudio']['puerto'] + ' RTP\r\n'
                line = METHOD + " sip:" + OPTION + ' SIP/2.0\r\n' + \
                    content_type_header + sip_body

                print()
                print("Sending:")
                print(line)
                my_socket.send(bytes(line, 'utf-8'))
                # Escribiendo en el log
                to_write = 'Sent to ' + ip + ':' + p + ': ' + \
                    line.replace('\r\n', ' ')
                log(config_data, to_write)

                data = my_socket.recv(1024)
                # Escribiendo en el log
                to_write = 'Received from ' + ip + ':' + p + ': ' + \
                    data.decode('utf-8').replace('\r\n', ' ')
                log(config_data, to_write)

                print('Received --', data.decode('utf-8'))
                chops = data.decode('utf-8').split()
                if len(chops) > 7 and chops[7] == '200':
                    line = 'ACK sip:' + OPTION + ' SIP/2.0\r\n\r\n'
                    print()
                    print("Sending:")
                    print(line)
                    my_socket.send(bytes(line, 'utf-8'))
                    # Escribiendo en el log
                    to_write = 'Sent to ' + ip + ':' + p + ': ' + \
                        line.replace('\r\n', ' ')
                    log(config_data, to_write)

                    # extraer datos sdp
                    rtp_ip = data.decode('utf-8').split()[13]
                    rtp_port = data.decode('utf-8').split()[17]
                    # envio RTP mediante hilos
                    thread1 = Thread(target=rtp, args=(rtp_ip, rtp_port,
                                     config_data['audio']['path'],))
                    # Reproducción mediante VLC con Hilos
                    thread2 = Thread(target=cvlc, args=(rtp_ip, '12345',))

                    thread1.start()
                    time.sleep(0.2)
                    thread2.start()

                    # Escribiendo en el log
                    to_write = 'Sent to ' + rtp_ip + ':' + rtp_port + ': ' + \
                        'RTP CONTENT'
                    log(config_data, to_write)

            elif METHOD == 'BYE':
                os.system('killall mp32rtp 2> /dev/null')
                os.system('killall vlc 2> /dev/null')

                line = METHOD + ' sip:' + OPTION + ' SIP/2.0\r\n\r\n'
                print()
                print("Sending:")
                print(line)
                my_socket.send(bytes(line, 'utf-8'))
                # Escribiendo en el log
                to_write = 'Sent to ' + ip + ':' + p + ': ' + \
                    line.replace('\r\n', ' ')
                log(config_data, to_write)

                data = my_socket.recv(1024)
                print('Received --', data.decode('utf-8'))
                # Escribiendo en el log
                to_write = 'Received from ' + ip + ':' + \
                    p + ': ' + data.decode('utf-8').replace('\r\n', ' ')
                log(config_data, to_write)

            elif METHOD not in ['REGISTER', 'INVITE', 'BYE']:
                print('Unrecognized method')
                print("Sending...")
                line = METHOD + " sip:" + \
                    config_data['account']['username'] + ':' + \
                    config_data['uaserver']['puerto'] + ' SIP/2.0\r\n\r\n'
                # Recibir respuesta
                my_socket.send(bytes(line, 'utf-8'))
                data = my_socket.recv(1024)
                print('Received --', data.decode('utf-8'))
                # Escribiendo en el log
                to_write = 'Received from ' + ip + ':' + \
                    p + ': ' + data.decode('utf-8').replace('\r\n', ' ')
                log(config_data, to_write)

    except ConnectionRefusedError:
        print('Error: No server listening at ' + ip + ' port ' + p)
        # Escribiendo en el log
        to_write = 'Error: No server listening at ' + ip + ' port ' + p
        log(config_data, to_write)

    print("Finished Socket.")
