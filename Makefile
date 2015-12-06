ccode.so: ccode.c
	gcc -shared -I/usr/include/python3.5m -lpython3 -o ccode.so ccode.c -fPIC
