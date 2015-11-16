#! /usr/bin/python

import re
import os

###Various examples of regular expression usage in python


#print os.listdir('.')


p=re.compile('ab*')
#print p
string='hello this is abbe age abe ae lincoln'
#print p.search(string).group()
#print p.search(string).start()
#print p.search(string).end()
#print p.search(string).span()

#p.findall(string)

#print re.search(r'ab',string).group()
# print re.findall(p, string)

p=re.compile('([\w.-]+)@([\w.-]+)') #groups
str = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'
#print p.findall(str)
#print p.sub('hello',str)
#print p.sub(r'\1@yo-yo-dyne.com', str)


ifile=open('text.txt','r')
p=re.compile('(\w+@(tickets\.)?company\.com)')
p=re.compile('([\w.-]+)@([\w.-]+)')
print p.findall(ifile.read())




