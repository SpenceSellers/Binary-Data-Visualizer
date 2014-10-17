ccode.so: ccode.c
	gcc -shared -I/usr/include/python2.7 -lpython2.7 -o ccode.so ccode.c -fPIC
