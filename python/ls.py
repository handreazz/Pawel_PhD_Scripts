#! /usr/bin/python
import sys
import os
from numpy import *


#######################################################################
# Script for getting list of files with expansion 
# Argument:
#          command - string variable of the ls command, eg 'ls *.pdb'
# Return:
#          output - list of all files  matching the ls command
#######################################################################

def ls(command):
	import subprocess
	import shlex
	import glob
	cmd='ls *txt'
	arg=shlex.split(cmd)
	arg = arg[:-1] + glob.glob(arg[-1])
	output = subprocess.check_output(arg)
	output=output.split()
	return output
