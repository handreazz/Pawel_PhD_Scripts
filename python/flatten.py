#! /usr/bin/python
import sys
import os
from numpy import *

def flatten(*args):
    x = []
    for l in args:
        if not isinstance(l, (list, tuple)): l = [l]
        for item in l:
            if isinstance(item, (list,tuple)):
                x.extend(flatten(item))
            else:
                x.append(item)
    return x
