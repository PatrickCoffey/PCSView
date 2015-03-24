#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - indivPerson
# ---------------------
# This is the individual client class

from distutils.core import setup
import py2exe
from glob import glob
import os
import sys


data_files = [("tutorial", glob(os.path.join(os.path.dirname(sys.argv[0]), 'tutorial', 'Using PCS View.htm'))),
              ("tutorial/Using PCS View_files", glob(os.path.join(os.path.dirname(sys.argv[0]), 'tutorial', 'Using PCS View_files', '*.*')))]
setup(
    data_files=data_files,
    windows=['PCSView.py']
)
