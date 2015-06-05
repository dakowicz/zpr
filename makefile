CFLAGS=-m64
CXXFLAGS=-m64
LDFLAGS=-m64

CardsCalculations: ./calculations/CardsCalculations.cpp
	g++ -I/usr/include/python2.7 -fpic ./calculations/CardsCalculations.cpp -shared -lboost_python -o ./calculations/pokerCalculations.so
