#include <stdlib.h>
#include <stdio.h>
#include <omp.h>


//**********************************************************************
/*                                                                    *
 * Print the max number of threads available to openmp on the system. *
 * Output printed to max_threads.txt.                                 *
 * Remember to compile with -fopenmp:                                 *  
 *    gcc -fopenmp -o print_max_threads print_max_threads.c           * 
 *                                                                    */  
//**********************************************************************
 

void main (int argc, char *argv[])
{
  int max_threads;
  max_threads = omp_get_max_threads();
  printf("The max num threads is %d\n", max_threads);
  FILE *f = fopen("max_threads.txt", "w");
  if (f == NULL)
  {
    printf("Error opening file!\n");
    exit(1);
  }
  fprintf(f, "The max num threads is %d\n", max_threads);
}
