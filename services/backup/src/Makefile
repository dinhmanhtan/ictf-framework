CFLAGS += -Wall
all: backup
clean:
	rm -f backup
backup: backup.c
	gcc -o backup backup.c -fPIE -pie
.PHONY: all clean
