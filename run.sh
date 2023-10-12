#estas son las instrucciones para compilar y ejecutar el programa 
#el compilador es gfortran

# performance
#gfortran -ofast -floop-parallelize-all -o output/main  functions.f90 algorithm.f90 main.f90

# debug
gfortran -g -O0 -Wall -o output/main functions.f90 algorithm.f90 main.f90
./output/main
