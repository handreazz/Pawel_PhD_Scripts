import sys, os
from numpy import mean

# number to test mcnuggets on
n = int(sys.argv[1])
print "Can we buy %d mcnuggets?\n" %n

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

#======================================================================#
# FIRST WAY: timeit
#======================================================================#
import timeit
def mytimer (func):
  n=100
  # This is a simple way to run n times and report total running time.
  print timeit.timeit (func, number =n)
  # A more versitile option uses Timer objet
  t = timeit.Timer(func)
  # Now just as timeit.timeit, report time to run n times
  print t.timeit(n)
  # repeat will run 10 sets of n trials and report a list of 10 times
  print mean(t.repeat(10,n))

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

# #First we need to wrap the function and arguments into a non-arguments function
# # so that we can feed it to timeit
# print "Checking mcnuggets 1"
# wrapped = wrapper(mcnuggets1, n)
# mytimer(wrapped)
#
# print "\nChecking mcnuggets 2"
# wrapped = wrapper(mcnuggets2, n)
# mytimer(wrapped)

#======================================================================#
# SECOND WAY: time
#======================================================================#
import time
def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print f.__name__, 'took', end - start, 'time'
        return result
    return f_timer

# using a decorator
@timefunc
def mcnuggets2_timed(n):
  return mcnuggets2(n)
print mcnuggets2_timed(n)

# which is the same as doing this
mcnuggets2_timed = timefunc(mcnuggets2)
print mcnuggets2_timed(n)

# or directly you can call
print timefunc(mcnuggets2)(n)



#======================================================================#
# DECORATOR with global variable
#======================================================================#
# # or you can set a variable like
# TIME=True
# def timefunc(f):
#     global TIME
#     print TIME
#     sys.exit()
#     def f_timer(*args, **kwargs):
#         start = time.time()
#         result = f(*args, **kwargs)
#         end = time.time()
#         print f.__name__, 'took', end - start, 'time'
#         return result
#     def f(*args, **kwargs):
#         result = f(*args, **kwargs)
#         return result
#     if TIME:
#       return f_timer
#     else:
#       return f
# @timefunc
# def mcnuggets2_timed(n):
#   return mcnuggets2(n)
# # TIME=True
# # print mcnuggets2_timed(n)
# # sys.exit()
# TIME=False
# print mcnuggets2_timed(n)
# sys.exit()

#======================================================================#
# DECORATOR with argument
#======================================================================#
def prettytimefunc(stopper=True):
  def wrapper_time(f):
    def f_timer(*args, **kwargs):
      start = time.time()
      result = f(*args, **kwargs)
      end = time.time()
      print f.__name__, 'took', end - start, 'seconds'
      return result
    return f_timer
  def wrapper_no_time(g):
    def f_no_timer(*args, **kwargs):
      result = g(*args, **kwargs)
      return result
    return f_no_timer
  if stopper:
    return wrapper_time
  else:
    return wrapper_no_time


@prettytimefunc(True)
def mcnuggets3(n):
  return mcnuggets2(n)

mcnuggets2_timed = prettytimefunc(True)(mcnuggets2)
mcnuggets2_not_timed = prettytimefunc(False)(mcnuggets2)

print 80*"="
print mcnuggets3(n)
print mcnuggets2_timed(n)
print mcnuggets2_not_timed(n)