#!/bin/sh

# if you simply want to see what command arguments are passed by subversion,
# simply uncomment following line, and comment rest of the script:
# echo "$@"

# http://pida.co.uk/wiki/UsingExternalDiffTools

# Configure your favorite diff program here.
DIFF="/usr/bin/meld"

# Subversion provides the paths we need as the sixth and seventh
# parameters.
LEFT=${3} # 'MINE' - was 6
RIGHT=${2} # 'THEIRS' (online) - was 7

# Call the diff command (change the following line to make sense for
# your merge program).
$DIFF $LEFT $RIGHT

# Return an errorcode of 0 if no differences were detected, 1 if some were.
# Any other errorcode will be treated as fatal.
