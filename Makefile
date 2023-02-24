CC=g++
CFLAGS=-c -Wall -ggdb3 -Wextra
FPIE=-fpie $$(python3-config --cflags --embed)
LDFLAGS=$$(python3-config --embed --ldflags)
GINC=-I./src
TARGETS=./src/main.o ./src/gremlin.o ./src/etc/settings.o ./src/etc/format.o ./src/mods/modbase.o ./src/mods/ank/ank.o

all: gremlin

gremlin: $(TARGETS)
	$(CC) $(FPIE) $(GINC) $^ -o $@ $(LDFLAGS)

