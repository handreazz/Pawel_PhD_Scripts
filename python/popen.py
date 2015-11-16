import subprocess

afitt_installed=False
x=subprocess.Popen(['which', 'afitt'],stdout=subprocess.PIPE)
if x.communicate()[0] != '':
  afitt_installed=True
  
if afitt_installed:
  print("AFITT is here.")  
