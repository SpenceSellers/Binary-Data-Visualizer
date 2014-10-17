#include <Python.h>
static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
    char *s = "Hello from C!";
    return Py_BuildValue("s", s);
}

    
int d2xy(int n, int d){
    int t = d;
    int x = 0;
    int y = 0;
    int s = 1;
    while (s < n){
        int rx = 1 & (t >> 1);
        int ry = 1 & (t ^ rx);
        if (ry == 0){
            if (rx == 1){
                x = s - 1 - x;
                y = s - 1 - y;
            }
        }

        x += s * rx;
        y += s * ry;
        t >>= 2;
        s <<= 1;
    }
    return y * n + x;

}

static PyObject* py_d2xy(PyObject* self, PyObject* args){
    int size;
    int index;
    
    PyArg_ParseTuple(args, "ii", &size, &index);

    int result = d2xy(size, index);
    return Py_BuildValue("b", result);
}


/*
 * Bind Python function names to our C functions
 */
static PyMethodDef ccode_methods[] = {
    {"myFunction", py_myFunction, METH_VARARGS},
    {"d2xy", py_d2xy, METH_VARARGS},
    //{"myOtherFunction", py_myOtherFunction, METH_VARARGS},
    {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
void initccode()
{
    (void) Py_InitModule("ccode", ccode_methods);
}