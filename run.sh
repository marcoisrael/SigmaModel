#estas son las instrucciones para compilar y ejecutar el programa 
#el compilador es gfortran
gfortran -ofast -floop-parallelize-all -o main fortran/m_progress_bar.f90 fortran/functions.f90 fortran/algorithm.f90 fortran/main.f90
./main