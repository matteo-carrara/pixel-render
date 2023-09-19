CC = gcc
CFLAGS = $(shell sdl2-config --cflags)
LIBS = $(shell sdl2-config --libs) -lGLEW -lglfw -lGL

# List of source files
SRCS = prog.c draw.c

# List of object files derived from source files
OBJS = $(SRCS:.c=.o)

# Output binary
TARGET = prog

# Build the program
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

# Rule to compile .c files to .o files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJS)

