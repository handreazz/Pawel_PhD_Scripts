import sys, os
import timeit
from numpy import mean

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def mcnuggets1(n):
  result = False
  if n<0:
    return False
  if n==0:
    return True
  if result == False:
    result = mcnuggets1(n-20)
  if result == False:
    result = mcnuggets1(n-9)
  if result == False:
    result = mcnuggets1(n-6)
  return result

def mcnuggets2(n):
  return ((n>-1) and (n==0 or mcnuggets2(n-20) or mcnuggets2(n-9) or mcnuggets2(n-6)))

def mytimer (func):
  # This is a simple way to run number times and report total running time.
  # print timeit.timeit (wrapped, number =1)

  # A more versitile option uses Timer objet
  t = timeit.Timer(func)
  # Now just as timeit.timeit, report time to run number times
  print t.timeit(100)
  # repeat will run 10 sets of 1000 trials and report a list of 10 times
  print mean(t.repeat(10,100))



# number to test mcnuggets on
n = int(sys.argv[1])
print "Can we buy %d mcnuggets?\n" %n

#First we need to wrap the function and arguments into a non-arguments function
# so that we can feed it to timeit
print "Checking mcnuggets 1"
wrapped = wrapper(mcnuggets1, n)
mytimer(wrapped)

print "\nChecking mcnuggets 2"
wrapped = wrapper(mcnuggets2, n)
mytimer(wrapped)

