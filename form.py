#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
# TLRTools- lib/TLRCombined.py
# ----------------------------
# This handles the filling of combined reports

import Tkinter

class mainForm(Tkinter.Tk):
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()
    
    def initialise(self):
        
        # Set grid
        self.grid()
        
        # set textentry
        self.tbHRN = Tkinter.Entry(self)
        self.tbHRN.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.tbFName = Tkinter.Entry(self)
        self.tbFName.grid(column=0, row=3, columnspan=2, sticky='EW')
        self.tbLName = Tkinter.Entry(self)
        self.tbLName.grid(column=0, row=5, columnspan=2, sticky='EW')        
        
        # set label
        lblHRN = Tkinter.Label(self, text="HRN:", anchor="centre", fg="white", bg="blue")
        lblHRN.grid(column=0, row=0, columnspan=2, sticky='EW')
        lblFName = Tkinter.Label(self, text="First Name:", anchor="centre", fg="white", bg="blue")
        lblFName.grid(column=0, row=2, columnspan=2, sticky='EW')
        lblLName = Tkinter.Label(self, text="Last Name:", anchor="centre", fg="white", bg="blue")
        lblLName.grid(column=0, row=4, columnspan=2, sticky='EW')
        
        # set button
        button = Tkinter.Button(self,text=u"Click me !")
        button.grid(column=1,row=0)
        
        # Resize controls with window resize
        self.grid_columnconfigure(0,weight=1)