#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from urllib.request import urlretrieve
from smallsmilhandler import SmallSMILHandler
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
try:
    default_json = sys.argv[1][:-4]+"json"
except:
    sys.exit("Usage: python3 karaoke.py file.smil")


class KaraokeLocal():

    def __init__(self, smil_file):

        self.datos = ""
        parser = make_parser()
        self.cHandler = SmallSMILHandler()
        parser.setContentHandler(self.cHandler)
        parser.parse(open(smil_file))
        self.atributes_list = self.cHandler.get_tags()

    def __str__(self):

        for ele in self.atributes_list:
            line = ele[0]
            atributos = ele[1]
            for at in ele[1]:
                if ele[1][at] != "":
                    line = line + '\t' + at + '=' + '"' + ele[1][at] + '"'
            print(line)
            self.datos += line

    def to_json(self, smil_file, json_file=default_json):

        json_file = open(json_file, 'w')
        json.dump(self.atributes_list, json_file)

    def do_local(self):

        for lista in self.atributes_list:
            atributos = lista[1]
            for at in atributos:
                if atributos[at][:7] == "http://":
                    urlretrieve(atributos[at], atributos[at].split('/')[-1])
                    atributos[at] = atributos[at].split('/')[-1]

if __name__ == "__main__":

    smil_file = sys.argv[1]
    karaoke_local = KaraokeLocal(smil_file)
    karaoke_local.__str__()
    karaoke_local.to_json(smil_file)
    karaoke_local.do_local()
    karaoke_local.to_json(smil_file, "local.json")
    karaoke_local.__str__()
