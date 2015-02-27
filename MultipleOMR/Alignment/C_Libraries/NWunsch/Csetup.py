'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

This file compiles 'NWunsch.c' into 'NWunsch.pyd'

The 'NWunsch.pyd' file should be copied in the'Alignment' folder

usage:

python Csetup.py  build
'''
from distutils.core import setup, Extension
 
module1 = Extension('NWunsch', sources = ['NWunsch.c'])
 
setup (name = 'NWunsch',
        version = '1.0',
        description = 'It calculates the differences between two arrays based on Needlemann Wunsh algorith',
        ext_modules = [module1])