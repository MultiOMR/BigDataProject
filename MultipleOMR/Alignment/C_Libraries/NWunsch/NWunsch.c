#include <stdio.h>
#include <stdlib.h>

#include <Python.h>


float needleman_wunsch_matrix(char* seq1[],char* seq2[],int n,int m)
{

    //int DIAG = 0;
    int UP = 1;
    int LEFT = 2;
    int score=0;

    int indel=-1;


    //ZERO MATRIX
    int i,j;

    int maxArray=n;
    if (m>n)
    {
        maxArray=m;
    }
    int memorySpace=2*maxArray+100;
    int **s;
    int **ptr;
    s =calloc(memorySpace , sizeof(int*));
    for (i = 0; i < memorySpace; i++)
        s[i] =  calloc(memorySpace,sizeof(int));

    ptr = (int**) calloc(memorySpace , sizeof(int));
    for (i = 0; i < memorySpace; i++)
        ptr[i] = calloc(memorySpace,sizeof(int));



    //INITIALIZE SCORING MATRIX

    for (i = 1; i <n+1; i++)
    {
        s[i][0]=indel*i;
    }
    for (j = 1; j <m+1; j++)
    {
        s[0][j]=indel*j;
    }
    //INITIALIZE TRACE BACK MATRIX
    for (i = 1; i <n+1; i++)
    {
        ptr[0][i]=LEFT;
    }
    for (j = 1; j <m+1; j++)
    {
        ptr[j][0]=UP;
    }
    //#####################################

    int p;
    int q;
    for (i = 1; i <n+1; i++)
    {
        p=i-350;
        q=i+350;
        if(p<1){
            p=1;
        }
        if(q>m+1)
        {
            q=m+1;
        }
        for(j=p;j<q;j++)
        {
            char* myseq1=seq1[i-1];
            char* myseq2=seq2[j-1];

            if(strcmp(myseq1,myseq2)==0)
            {
                score=1;
            }else{
                score=-1;
            }

            s[i][j]=s[i-1][j-1]+score;

            if(s[i-1][j]+indel>s[i][j])
            {
                s[i][j]=s[i-1][j]+indel;
                ptr[i][j]=UP;
            }
            if(s[i][j-1]+indel>s[i][j])
            {
                s[i][j]=s[i][j-1]+indel;
                ptr[i][j]=LEFT;

            }

        }

    }

    float finalScore;
    finalScore=(float)s[n][m]/(float)maxArray;

    for (i = 0; i < memorySpace; i++){
        free(s[i]);
    }
    free(s);
    for (i = 0; i < memorySpace; i++){
        free(ptr[i]);
    }
    free(ptr);
    return finalScore;

}


static PyObject *
NWunsch_getSimilarity(PyObject* self, PyObject* args)
{
	
    PyObject   *t1,*t2;
    int t_seqlen1=0;
    int t_seqlen2=0;
    int  i;
    PyObject *x_obj,*y_obj;
    


    if (!PyArg_ParseTuple(args, "OO", &x_obj, &y_obj))
        return NULL;
        
    //Sequence 1
    t1 = PySequence_Fast(x_obj, "argument must be iterable");
    t_seqlen1 = PySequence_Fast_GET_SIZE(t1);

    int width=1;
    char **align1 =(char **)malloc(t_seqlen1 * sizeof(char*));
    *align1 = malloc(t_seqlen1 * width * sizeof(char));
    for (i = 0; i < t_seqlen1; i++)
    {
        align1[i] =  *align1 + i*width;
        align1[i]=PyString_AsString(PySequence_Fast_GET_ITEM(t1, i));;
    }


    //Sequence 2
    t2 = PySequence_Fast(y_obj, "argument must be iterable");
    t_seqlen2 = PySequence_Fast_GET_SIZE(t2);


    char **align2 =(char **)malloc(t_seqlen2 * sizeof(char*));
    *align2 = malloc(t_seqlen2 * width * sizeof(char));
    for (i = 0; i < t_seqlen2; i++)
    {
    	align2[i] =  *align2 + i*width;
    	align2[i]=PyString_AsString(PySequence_Fast_GET_ITEM(t2, i));
    }



    float score;
    score=needleman_wunsch_matrix(align1,align2,t_seqlen1,t_seqlen2);
    
    free(*align1);
    free(align1);

	free(*align2);
	free(align2);

	Py_XDECREF(t1);
	Py_XDECREF(t2);
	



    return Py_BuildValue("f", score);
}


static PyMethodDef NWunschMethods[] =
{
     {"NWunsch_getSimilarity", NWunsch_getSimilarity, METH_VARARGS, "NWunsch_getSimilarity"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initNWunsch(void)
{
     (void) Py_InitModule("NWunsch", NWunschMethods);
}


