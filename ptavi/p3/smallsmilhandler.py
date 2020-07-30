#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class SmallSMILHandler(ContentHandler):

    def __init__(self):

        self.atributes_list = []
        self.tags = []

    def startElement(self, name, attrs):

        info_smil = {}
        atributes_1 = {'width', 'height', 'background-color'}
        atributes_2 = {'id', 'top', 'left', 'boottom', 'right'}
        atributes_3 = {'src', 'region', 'begin', 'dur'}
        atributes_4 = {'src', 'begin', 'dur'}
        atributes_5 = {'src', 'region'}
        tags = {'root-layout': atributes_1, 'region': atributes_2,
                'img': atributes_3, 'audio': atributes_4,
                'textstream': atributes_5}
        if name in tags:
            self.tags.append(name)
            for atribute in tags[name]:
                info_smil[atribute] = attrs.get(atribute, "")
            self.atributes_list.append([name, info_smil])

    def get_tags(self):
        return self.atributes_list

if __name__ == "__main__":

    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open('karaoke.smil'))
    print(cHandler.get_tags())
