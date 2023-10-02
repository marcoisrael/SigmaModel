#estas son las instrucciones para compilar y ejecutar el programa 
#el compilador es gfortran
gfortran -ofast -floop-parallelize-all -o sigma-model fortran/m_progress_bar.f90 fortran/functions.f90 fortran/method.f90 fortran/sigma-model.f90
./sigma-model