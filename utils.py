#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
# TLRTools- lib/TLRCombined.py
# ----------------------------
# This handles the filling of combined reports

import bs4
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from HTMLParser import HTMLParser

class app(object):
    inFile = ''
    HRNMap = {}
    NameMap = {}
    clients = {}
    
    def __init__(self, inFile='test.html'):
        self.inFile = inFile
        self.parseHTML

    def getDataForMap(self, html):
        HRNMap = {} 
        NameMap = {}
        soup = bs4.BeautifulSoup(html)
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
                #print("+++" + str(counter) + br)
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


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def getClientfrom(string, Map):
    ret = Map.get(string)
    return ret

def yieldHTML(inFile='test.html'):
    f = file
    with open(inFile, 'r') as f:
        text = str(f.read()).strip('\n')
        startIndex = text.find('<body>') + 6
        stopIndex = text.find('</body>')
        text = text[startIndex: stopIndex]
        delim = text.split('<br />')
        counter = 1
        temp = ''
        clients = []
        for br in delim:
            if counter == 12:
                clients.append(temp)
                temp = ''
                counter = 1
            temp += br
            counter += 1
        for client in clients:
            yield client

def encryptToFile(in_file, out_file, password, key_length=32):
    """
    to EncryptToFile:
    with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
        encrypt(in_file, out_file, password)
    """    
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decryptToFile(in_file, out_file, password, key_length=32):
    """
    to DecryptToFile:
    with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
        decrypt(in_file, out_file, password)
    """    
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)

def encrypt(in_file, password, key_length=32):
    """
    to Encrypt:
    with open(in_filename, 'rb') as in_file:
        encrypted = encrypt(in_file, password)
    """
    ret = ''
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = 'Salted__' + salt
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        ret += (cipher.encrypt(chunk))
    return ret

def decrypt(in_file, password, key_length=32):
    """
    to Decrypt:
    with open(in_filename, 'rb') as in_file:
        decrypted = decrypt(in_file, password)
    """
    ret = ''
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        ret += chunk
    return chunk

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

if __name__ == '__main__':

    test = app()
    test.parseHTML()
    for key, client in test.clients.iteritems():
        print('STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART')
        print('HRN: ' + str(test.HRNMap[key]))
        print('Name: ' + str(test.NameMap[key]))
        print(client)
        print('ENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND')