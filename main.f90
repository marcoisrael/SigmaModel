program main
use algorithm
use functions
real(8), allocatable, dimension(:,:,:) :: s
real(8) :: temperature
integer :: N, thermalization, cycles
character(60) path
LENGTH = 8
VOLUME = LENGTH*LENGTH
thermalization = 1e3
temperature = 0.1
beta = 1/temperature
cycles = 100
N = 10
path = "output/data/therm.csv"
allocate(s(LENGTH,LENGTH,3))
call hot_start(s)
open(unit=1, file=trim(path))
do i=1, cycles
    med(1) = 0
    var(1) = 0
    do j=1, N
        obs(1) = system_energy(s)
        med(1) = med(1)+obs(1)
        var(1) = var(1)+obs(1)**2
        call step_metropolis(s)
    end do
    med(1) = med(1)/N
    var(1) = (var(1)-N*med(1)**2)/(N-1)
    write(1,"(2(f0.16,:,','))") med(1), sqrt(var(1)/N)
end do
end program