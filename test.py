#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
import fileinput
from cStringIO import StringIO

with open('test2.dec.html', 'rb') as fin:
    shtml = ''
    for line in fin:
        shtml += line
    opener = "<"
    closer = "</"
    tags = ['html','body', 'div','h1','center','table','tr','td','b']
    for tag in tags:
        topen = opener + tag
        fopen = str(shtml.lower()).split(topen)
        nopen = len(fopen) -1
        tclose = closer + tag
        fclose = str(shtml.lower()).split(tclose)
        nclose = len(fclose) -1
        print(tag + '= open: ' + str(nopen) + ' close: ' + str(nclose) + ' diff: ' + str(nclose - nopen))
    #fout.write(shtml.replace(find, replace))
    
#shtml = ''

#with open('test.html', 'rb') as fin:
    #shtml = fin.read()
    

##for line in fileinput.input(['test.html']):


#parser = etree.HTMLParser(recover=False)
#startIndex = shtml.find('<body>') + 6
#stopIndex = shtml.find('</body>')
#shtml = shtml[startIndex: stopIndex].strip('\r\n')
#temp = shtml.splitlines()
#print(len(temp))
#tree = etree.HTML(shtml)
#print(etree.tostring(tree))