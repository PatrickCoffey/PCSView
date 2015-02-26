#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - indivPerson
# ---------------------
# This is the individual client class

from indivPerson import IndivPerson
from utils import *
from form import mainForm

if __name__=='__main__':
    test = mainForm(None)
    test.title('Main.py')
    test.mainloop()