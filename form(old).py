#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - form.py
# -----------------
# This is the forms and parser for the project.


import Tkinter
import webbrowser
import tkFileDialog
import bs4
from HTMLParser import HTMLParser
import itertools

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
    results = []
    HRNMap = {}
    NameMap = {}
    clients = {}
    pages = []
    page = 0
    def initialise(self):
        
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
        self.btnSearch.grid(column=3, row=3, columnspan=2)
        self.btnClear = Tkinter.Button(self, text=u"Clear", command=self.clearTable)
        self.btnClear.grid(column=3, row=1, columnspan=2)
        
        # set Table
        self.table = SimpleTable(self)
        self.table.grid(column=0, row=5, rowspan=5, columnspan=4, sticky='EW')
        
        # set bottom buttons
        self.btnFirst = Tkinter.Button(self, text=u"First")
        self.btnFirst.grid(column=0, row=10, columnspan=1, sticky='EW')
        self.btnPrev = Tkinter.Button(self, text=u"Prev")
        self.btnPrev.grid(column=1, row=10, columnspan=1, sticky='EW')
        self.btnNext = Tkinter.Button(self, text=u"Next")
        self.btnNext.grid(column=2, row=10, columnspan=1, sticky='EW')
        self.btnLast = Tkinter.Button(self, text=u"Last")
        self.btnLast.grid(column=3, row=10, columnspan=1, sticky='EW')
        
        # Resize controls with window resize
        self.grid_columnconfigure(0,weight=1,minsize=100)
        self.grid_columnconfigure(1,weight=1,minsize=100)
        self.grid_columnconfigure(2,weight=1,minsize=100)
        self.grid_columnconfigure(3,weight=1,minsize=100)
        
    def loadData(self):
        self.HTMLFile = tkFileDialog.askopenfilename(defaultextension='.html', initialdir='C:/temp/', title='Choose Mass Client Summary', parent=self)
        self.parseHTML()
    
    def _first(self):
        pass
    
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

    def parseHTML(self):
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
    
    def _splitPages(self, size=4):
        it = iter(self.results)
        item = list(itertools.islice(it, size))
        while item:
            self.pages.append(item)
            item = list(itertools.islice(it, size))        
    
    def updateTable(self):
        row = 1
        for res in self.pages[self.page]:
            key = res[0]
            hrn = res[1]
            name = res[2]
            self.table.set(row, 0, hrn)
            self.table.set(row, 1, name)
            row += row
            
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
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
        self.set(0, 0, 'HRN')
        self.set(0, 1, 'Name')
    
    def clear(self):
        for row in range(1, self.rows):
            for col in range(self.columns):
                widget = self._widgets[row][col]
                widget.configure(text='')
            
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)