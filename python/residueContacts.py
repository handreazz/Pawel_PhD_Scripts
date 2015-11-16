#! /usr/bin/python
import commands

class ifaces:
	def __init__(self,files):
		self.all=[]
		for file in files:
			f=open(file)
			for line in f.readlines():
				if line[0]=='S':
					if line.split()[1] not in self.all:
						self.all.append(line.split()[1])
					if 	line.split()[1] == 'x-4,y-1,z-2':
						print file
	

			
if __name__ == "__main__" :
	test=commands.getoutput('ls -1 /home/pjanowsk/c/Case/4lzt/RunSi/average_density/residueContacts5.5/*dat').split()
	#6000files=2min
	import code; code.interact(local=locals())
	interfaces=ifaces(test)
	print interfaces.all



