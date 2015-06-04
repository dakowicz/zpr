CFLAGS=-m64
CXXFLAGS=-m64
LDFLAGS=-m64

CardsCalculations: CardsCalculations.cpp
	g++ -I/usr/include/python2.7 -fpic CardsCalculations.cpp -shared -lboost_python -o pokerCalculations.so

clean:
	rm -f *.so *.o