#estas son las instrucciones para compilar y ejecutar el programa 
#el compilador es gfortran
gfortran -ofast -floop-parallelize-all -o main  functions.f90 algorithm.f90 main.f90
./main