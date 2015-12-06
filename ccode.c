#include <Python.h>
#include <stdlib.h>
#include <stdio.h>

static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
    char *s = "Hello from C!";
    return Py_BuildValue("s", s);
}

unsigned char maxChar(unsigned char a, unsigned char b){
    if (a > b){
        return a;
    } else {
        return b;
    }
}

int d2xy(int n, int d){
    int t = d;
    int x = 0;
    int y = 0;
    int s = 1;
    while (s < n){
        int rx = 1 & (t >> 1);
        int ry = 1 & (t ^ rx);
        if (ry == 0 && rx == 1){
            x = s - 1 - x;
            y = s - 1 - y;
        }

        x += s * rx;
        y += s * ry;
        t >>= 2;
        s <<= 1;
    }
    return y * n + x;
}

int *preloaded;

static PyObject *py_hilbert_preload(PyObject* self, PyObject* args){
    int size;
    PyArg_ParseTuple(args, "i", &size);


    int number = pow(size, 2);
    preloaded = malloc(sizeof(int) * number);
    int i;
    for (i = 0; i < number; i++){
        preloaded[i] = d2xy(size, i);
        //printf("Yeah %d %d\n", i, preloaded[i]);
    }

    return Py_BuildValue("b", 0);

}

static PyObject* py_d2xy(PyObject* self, PyObject* args){
    int size;
    int index;

    PyArg_ParseTuple(args, "ii", &size, &index);

    int result = d2xy(size, index);
    return Py_BuildValue("b", result);
}

static PyObject* py_get_preloaded(PyObject* self, PyObject* args){
    int index;

    PyArg_ParseTuple(args, "i", &index);

    int result = preloaded[index];
    return Py_BuildValue("b", result);
}

static PyObject* py_weirdMap(PyObject* self, PyObject* args){
    unsigned char val;
    PyArg_ParseTuple(args, "b", &val);

    unsigned char red = maxChar((val >> 7) * 255, val >> 4);
    unsigned char green = val;
    unsigned char blue = (val & 15) * 16;

    PyObject *t = Py_BuildValue("(bbb)", red, green, blue);

    return t;
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef ccode_methods[] = {
    {"myFunction", py_myFunction, METH_VARARGS},
    {"d2xy", py_d2xy, METH_VARARGS},
    {"weirdMap", py_weirdMap, METH_VARARGS},
    {"preload", py_hilbert_preload, METH_VARARGS},
    {"get_preloaded", py_get_preloaded, METH_VARARGS},
    //{"myOtherFunction", py_myOtherFunction, METH_VARARGS},
    {NULL, NULL}
};

static struct PyModuleDef ccode_module = {
    PyModuleDef_HEAD_INIT,
    "ccode",
    NULL,
    -1,
    ccode_methods,
    NULL,
    NULL,
    NULL,
    NULL
};
/*
 * Python calls this to let us initialize our module
 */
PyMODINIT_FUNC
PyInit_ccode(void)
{
    return PyModule_Create(&ccode_module);
}
