#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - indivPerson
# ---------------------
# This is the individual client class

from indivPerson import IndivPerson
from utils import *
from form import mainForm
import sys
import os
import Tkinter

if __name__=='__main__':
    main = mainForm(None)
    main.title('PCS Viewer - No data loaded...')
    main.mainloop()
