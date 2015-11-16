#!/usr/bin/env python
import os
from numpy import *
from Scientific.IO import NetCDF
from ReadAmberFiles import *
import argparse

pawel='''
  -1.0442      14.3708      24.0721     1     1   
  -11.9225      10.9527      56.3471     2     1   
  -12.9261      43.9430      24.0721     3     1   
  -23.8045      40.5249      56.3471     4     1   
   26.1958      14.3708      24.0721     5     1   
   15.3175      10.9527      56.3471     6     1   
   14.3139      43.9430      24.0721     7     1   
    3.4355      40.5249      56.3471     8     1   
   53.4358      14.3708      24.0721     9     1   
   42.5575      10.9527      56.3471    10     1   
   41.5539      43.9430      24.0721    11     1   
   30.6755      40.5249      56.3471    12     1   
'''
p=array([i.split()[0:3] for i in pawel.split('\n') if i], dtype=float32)

