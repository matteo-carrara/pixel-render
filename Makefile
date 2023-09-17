CC = gcc
CFLAGS = $(shell sdl2-config --cflags)
LIBS = $(shell sdl2-config --libs)

prog: prog.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f prog

