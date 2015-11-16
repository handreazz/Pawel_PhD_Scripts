# location of the Python header files
 
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
 
# location of the Boost Python include files and library
 
BOOST_INC = /usr/include
BOOST_LIB = /usr/lib64
 
# compile mesh classes
TARGET1 = vector
TARGET2 = hello_ext
TARGET3 = vector2
 
#$(TARGET).so: $(TARGET).o
#	g++ -shared -Wl,--export-dynamic $(TARGET).o -L$(BOOST_LIB) -lboost_python -L/usr/lib64/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET).so
 
#$(TARGET).o: $(TARGET).cpp
#	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp


.PHONY: ALL
ALL: $(TARGET1).so $(TARGET2).so $(TARGET3).so


$(TARGET1).so: $(TARGET1).cpp
	g++ -shared -Wl,--export-dynamic $(TARGET1).cpp -L$(BOOST_LIB) -lboost_python -L/usr/lib64/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET1).so -I$(PYTHON_INCLUDE) -fPIC
	
$(TARGET2).so: $(TARGET2).cpp
	g++ -shared -Wl,--export-dynamic $(TARGET2).cpp -L$(BOOST_LIB) -lboost_python -L/usr/lib64/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET2).so -I$(PYTHON_INCLUDE) -fPIC	

$(TARGET3).so: $(TARGET3).cpp
	g++ -shared -Wl,--export-dynamic $(TARGET3).cpp -L$(BOOST_LIB) -lboost_python -L/usr/lib64/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET3).so -I$(PYTHON_INCLUDE) -fPIC	
