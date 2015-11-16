from pymol import cmd

# run from script dir:
import os
def Run(filename):
    for Path in ['',
os.path.expanduser('~/c/scripts/pymol/')]:
        full = os.path.join(Path, filename)
        if os.path.exists(full):
            cmd.do('run ' + full)
            return
    print ' Error: no such file: {0}'.format(filename)
cmd.extend('Run', Run)
