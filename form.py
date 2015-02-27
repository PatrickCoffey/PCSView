#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - form.py
# -----------------
# This is the forms and parser for the project.


import Tkinter
import webbrowser
import tkFileDialog
import tkSimpleDialog
import bs4
from HTMLParser import HTMLParser
import itertools
import utils
import tempfile
import os

class form(Tkinter.Tk):
    """
    Form
    ----
    This is the base form class with a couple of 
    special methods for inheriting"""
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()
        
        
    def initialise(self):
        '''Overload this method and init controls!'''
        pass

class mainForm(form):
    """
    mainForm
    --------
    This is the application
    """
    currHRN = ''
    currName = ''
    currHTML = ''
    results = []
    HRNMap = {}
    NameMap = {}
    clients = {}
    pages = []
    page = 0
    def initialise(self):
        # set up temp dir
        self.tempDir = tempfile.gettempdir()
        self.tempFileURL = os.path.join(self.tempDir, 'currClient.html')
        
        # Set grid
        self.grid()
        
        # Set menubar
        self.menubar = Tkinter.Menu(self)
        filemenu = Tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.loadData)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label='File', menu=filemenu)
        self.config(menu=self.menubar)
        
        # set textentry
        self.tbHRN = Tkinter.Entry(self)
        self.tbHRN.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.tbName = Tkinter.Entry(self)
        self.tbName.grid(column=0, row=3, columnspan=2, sticky='EW')
        
        # set label
        lblHRN = Tkinter.Label(self, text="HRN:", anchor="w")
        lblHRN.grid(column=0, row=0, columnspan=2, sticky='EW')
        lblName = Tkinter.Label(self, text="Name:", anchor="w")
        lblName.grid(column=0, row=2, columnspan=2, sticky='EW')
        
        # set top buttons
        self.btnSearch = Tkinter.Button(self, text=u"Search", command=self.refresh)
        self.btnSearch.grid(column=3, row=2, columnspan=2)
        self.btnClear = Tkinter.Button(self, text=u"Clear", command=self.clearTable)
        self.btnClear.grid(column=3, row=1, columnspan=2)
        self.btnSelect = Tkinter.Button(self, text=u"Select", command=self.select)
        self.btnSelect.grid(column=3, row=4, columnspan=2)

        # set Table
        self.table = SimpleTable(self)
        self.table.grid(column=0, row=5, rowspan=5, columnspan=4, sticky='EW')
        
        # set bottom buttons
        self.btnFirst = Tkinter.Button(self, text=u"First", command=self._first)
        self.btnFirst.grid(column=0, row=10, columnspan=1, sticky='EW')
        self.btnPrev = Tkinter.Button(self, text=u"Prev", command=self._prev)
        self.btnPrev.grid(column=1, row=10, columnspan=1, sticky='EW')
        self.btnNext = Tkinter.Button(self, text=u"Next", command=self._next)
        self.btnNext.grid(column=2, row=10, columnspan=1, sticky='EW')
        self.btnLast = Tkinter.Button(self, text=u"Last", command=self._last)
        self.btnLast.grid(column=3, row=10, columnspan=1, sticky='EW')
        
        # Resize controls with window resize
        self.grid_columnconfigure(0,weight=1,minsize=100)
        self.grid_columnconfigure(1,weight=1,minsize=100)
        self.grid_columnconfigure(2,weight=1,minsize=100)
        self.grid_columnconfigure(3,weight=1,minsize=100)
        
    def loadData(self):
        '''Loads data'''
        #self.HTMLFile = tkFileDialog.askopenfilename(defaultextension='.html', initialdir='C:/temp/', title='Choose Mass Client Summary', parent=self)
        encodedFilename = tkFileDialog.askopenfilename(defaultextension='.html', initialdir='C:/temp/', title='Choose Mass Client Summary', parent=self)
        passwd = tkSimpleDialog.askstring('Enter Password', 'Please Enter the password.\n\nNote: make sure it is correct!')
        with open(encodedFilename, 'rb') as f:
            HTMLRaw = utils.decrypt(f, passwd)
        self.parseDIV(HTMLRaw)
    
    def _first(self):
        self.page = 0
        self.updateTable()
        
    def _prev(self):
        self.page += -1
        if self.page < 0:
            self.page = 0
        self.updateTable()
        
    def _next(self):
        self.page += 1
        if self.page > (len(self.pages) - 1):
            self.page = len(self.pages) - 1
        self.updateTable() 
        
    def _last(self):
        self.page = len(self.pages) - 1
        self.updateTable()
    
    def select(self):
        if self.table.selected == None or self.table.selected == '':
            return
        self.getCurrHTML()
        self._showHTML()

    def _showHTML(self):
        if os.path.exists(self.tempFileURL):
            os.remove(self.tempFileURL)
        with open(self.tempFileURL, 'wb') as f:
            f.write(self.currHTML)
        webbrowser.open(self.tempFileURL)
    
    def refresh(self):
        tempHRN = self.tbHRN.get()
        if tempHRN == '':
            self.currHRN = None
        else:
            self.currHRN = tempHRN  
        tempName = self.tbName.get()
        if tempName == '':
            self.currName = None
        else:
            self.currName = tempName
        self.getClient()
        
    def getDataForMap(self, html):
        HRNMap = {} 
        NameMap = {}
        if html == '\r\n' or html == '\n\n' or html == '\n':
            return
        soup = bs4.BeautifulSoup(html, "html.parser")
        demo = soup.contents[3].contents[1].contents[1].contents[1].contents[1]
        
        self.HRNMap[self.key] = demo.contents[7].contents
        if len(self.HRNMap[self.key]) == 0:
            self.HRNMap[self.key] = ''
        else:
            if isinstance(self.HRNMap[self.key], list):
                self.HRNMap[self.key] = str(self.HRNMap[self.key][0])
        
        self.NameMap[self.key] = demo.contents[3].contents
        if len(self.NameMap[self.key]) == 0:
            self.NameMap[self.key] = ''
        else:
            if isinstance(self.NameMap[self.key], list):
                self.NameMap[self.key] = str(self.NameMap[self.key][0])

    def parseHTML(self, text=None):
        if text == None:
            return None
        text = str(text).strip('\n')
        startIndex = text.find('<body>') + 6
        stopIndex = text.find('</body>')
        text = text[startIndex: stopIndex]
        #print(text)
        delim = text.split('<br />')
        counter = 0
        temp = ''
        self.key = 0         
        for br in delim:
            #print("+++" + str(counter) + br)
            if br == '\n':
                continue
            counter += 1
            temp += br
            if counter == 1:
                self.getDataForMap(br)
            if counter == 11:
                self.clients[self.key] = temp
                temp = ''
                counter = 0
                self.key += 1

    def parseDIV(self, text=None):
        if text == None:
            return None
        text = str(text).strip('\n')
        startIndex = text.find('<body>') + 6
        stopIndex = text.find('</body>')
        text = text[startIndex: stopIndex]
        for client in text.find() findall('DIV'):
            print(client)

    def parseHTMLFile(self):
        f = file
        with open(self.HTMLFile, 'r') as f:
            text = str(f.read()).strip('\n')
            startIndex = text.find('<body>') + 6
            stopIndex = text.find('</body>')
            text = text[startIndex: stopIndex]
            #print(text)
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
                
    def getClient(self):
        if self.currHRN != None:
            for key, hrn in self.HRNMap.iteritems():
                if hrn == self.currHRN:
                    self.results.append([key, hrn, self.NameMap[key]])
        if len(self.results) == 0:
            if self.currName != None:
                for key, name in self.NameMap.iteritems():
                    if self.currName in name:
                        self.results.append([key, self.HRNMap[key], name])
        self._splitPages()
        self.updateTable()
        
    def getCurrHTML(self):
        self.currHTML = ''
        if self.table.selected != None:
            for key, name in self.NameMap.iteritems():
                if name == self.table.selected:
                    self.table.selected = self.HRNMap[key]            
            for key, hrn in self.HRNMap.iteritems():
                if hrn == self.table.selected:
                    self.currHTML = self.clients[key]
                    return

    def _splitPages(self, size=4):
        it = iter(self.results)
        item = list(itertools.islice(it, size))
        while item:
            self.pages.append(item)
            item = list(itertools.islice(it, size))        
    
    def updateTable(self):
        row = 1
        if self.pages != []:
            self.clearTable()
            for res in self.pages[self.page]:
                key = res[0]
                hrn = res[1]
                name = res[2]
                self.table.set(row, 0, hrn)
                self.table.set(row, 1, name)
                row += 1
            
    def clearTable(self):
        self.table.clear()
        
class SimpleTable(Tkinter.Frame):
    
    def __init__(self, parent, rows=5, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        Tkinter.Frame.__init__(self, parent, background="black")
        self._widgets = []
        self.rows = rows
        self.columns = columns
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = Tkinter.Label(self, text='', borderwidth=0)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                label.bind('<Button-1>', self._tableClick)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
        self.set(0, 0, 'HRN')
        self.set(0, 1, 'Name')
        
    def _tableClick(self, event):
        text = event.widget.cget('text')
        self.selected = text
  
    def clear(self):
        for row in range(1, self.rows):
            for col in range(self.columns):
                widget = self._widgets[row][col]
                widget.configure(text='')
            
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)