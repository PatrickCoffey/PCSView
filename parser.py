#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - parser
# ----------------
# This is the individual client class

import bs4
from HTMLParser import HTMLParser

class PCSParser(object):
    inFile = ''
    HRNMap = {}
    NameMap = {}
    clients = {}
    
    def __init__(self, inFile=''):
        self.inFile = inFile

    def getDataForMap(self, html):
        HRNMap = {} 
        NameMap = {}
        soup = bs4.BeautifulSoup(html, "html.parser")
        demo = soup.contents[3].contents[1].contents[1].contents[1].contents[1]
        self.HRNMap[self.key] = str(demo.contents[7].contents)
        self.NameMap[self.key] = str(demo.contents[3].contents)

    def parseHTML(self):
        f = file
        with open(self.inFile, 'r') as f:
            text = str(f.read()).strip('\n')
            startIndex = text.find('<body>') + 6
            stopIndex = text.find('</body>')
            text = text[startIndex: stopIndex]
            delim = text.split('<br />')
            counter = 1
            temp = ''
            self.key = 0         
            for br in delim:
                if br == '\n':
                    continue
                if counter == 1:
                    self.getDataForMap(br)
                counter += 1
                if counter == 12:
                    self.clients[self.key] = temp
                    temp = ''
                    counter = 1
                    self.key += 1
                temp += br
                
    def getClient(self, hrn=None, name=None):
        pass