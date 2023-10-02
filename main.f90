program main
use algorithm
use functions
real(8), allocatable, dimension(:,:,:) :: s
real(8) :: temperature
integer :: N, thermalization, cycles
character(60) path
LENGTH = 8
VOLUME = LENGTH*LENGTH
thermalization = 1e2
temperature = 1
beta = 1/temperature
cycles = 200
N = 100
path = "output/file/therm.csv"
allocate(s(LENGTH,LENGTH,3))
call hot_start(s)
open(unit=1, file=trim(path))
do i=1, cycles
    write(1,"(f0.16)") system_energy(s)
    call step_metropolis(s)
end do
end program