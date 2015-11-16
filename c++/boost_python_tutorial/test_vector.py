#! /usr/bin/python

import vector
lint=[1,2,3,4]
print vector.reverse_list(lint)

double_vector = vector.VectorOfDouble()
double_vector.extend(arg for arg in lint)
vector.firstelement(double_vector)
print double_vector
print list(double_vector)


lstring=['hello','hi there', 'bye']
str_vector=vector.XVec()
str_vector.extend(vector.X(arg) for arg in lstring)

for i in str_vector:
	print vector.x_value(i)


y=vector.pointer(double_vector)
print y
