
EXECUTABLES=ex1 ex2 ex3 ex4 ex5 ex6 ex7 ex8 ex9 ex10
.PHONY=clean distclean

all: $(EXECUTABLES)

ex2: ex2.o ex2_helloworld.o
	$(CXX) -o $@ $@.o ex2_helloworld.o

.cpp.o:
	$(CXX) $(CXXFLAGS) $< -c -o $@

.o:
	$(CXX) $(CXXFLAGS)  $(LDFLAGS) -o $< $@.o

clean:
	rm -f $(EXECUTABLES) *.o

distclean: clean
	rm -f *~
