CC = gcc
CXX = g++
CFLAGS = -Wall -g -O2 -O3 -DENABLE_THREADS -D_REENTRANT
LIBS =  -lircclient -lpthread  -lnsl



bot:		bot.cpp
	$(CXX) -o bot bot.cpp $(LIBS) $(CFLAGS)

