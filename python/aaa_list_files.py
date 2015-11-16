print "hello pawel"
from os import walk
mypath = "."
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    print "/%s" %dirpath
    for file in filenames:
        print "    %s" %file
    print ""
 #   f.extend(filenames)
 #   break
#n = open("filelist
