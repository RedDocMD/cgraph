all: test1 test2

test1: test1.c
	gcc -o test1 test1.c -Wall -O3

test2: test2.c
	gcc $(shell pkg-config --cflags gtk4) -Wall -O3 -o test2 test2.c $(shell pkg-config --libs gtk4)