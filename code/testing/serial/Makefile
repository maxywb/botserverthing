CC=gcc
CFLAGS=-I. -lserial -ggdb
RAMP=ramptest.cpp 
DBTEST=dbtest.cpp 
SERIAL=serialtest.cpp 

ramp: $(RAMP)
	gcc -o $@ $^ $(CFLAGS)

dbtest: $(DBTEST)
	gcc -o $@ $^ $(CFLAGS)
serial: $(SERIAL)
	gcc -o $@ $^ $(CFLAGS)
