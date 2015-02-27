from distutils.core import setup
import sys
import py2exe
import numpy

    

from glob import glob
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
sys.path.append("C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

setup(
    data_files=data_files,
    
    console=['mainGDI.py'],

  )
