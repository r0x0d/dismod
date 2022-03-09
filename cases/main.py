import os 
import sys
from os.path import join 

def func_import(): 
    import pathlib

def try_expect_import():
    try: 
        import test_module 
    except ModuleNotFoundError:
        pass 