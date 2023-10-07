program main
use algorithm
use functions
real(8), allocatable, dimension(:,:,:) :: s
real(8) :: temperature
integer :: N, thermalization, cycles
! character(60) path
LENGTH = 8
VOLUME = LENGTH*LENGTH
thermalization = 1e3
temperature = 4.
beta = 1/temperature
cycles = 100
N = 2e5
allocate(s(LENGTH,LENGTH,3))

! Metropolis
med = 0
var = 0
call hot_start(s)
do i=1, thermalization
    call metropolis(s)
end do
do i=1, N
    obs = system_charge(s)**2
    med = med+obs
    var = var+obs**2
    call metropolis(s)
end do
med = med/N
var = (var-N*med**2)/(N-1)
print "((A20),*(f20.16))", "Metropolis", med, sqrt(var/N)  

! Random metropolis
med = 0
var = 0
call hot_start(s)
do i=1, thermalization
    call random_metropolis(s)
end do
do i=1, N
    obs = system_charge(s)**2
    med = med+obs
    var = var+obs**2
    call random_metropolis(s)
end do
med = med/N
var = (var-N*med**2)/(N-1)
print "((A20),*(f20.16))", "Random Metropolis", med, sqrt(var/N) 

! Glauber
med = 0
var = 0
call hot_start(s)
do i=1, thermalization
    call glauber(s)
end do
do i=1, N
    obs = system_charge(s)**2
    med = med+obs
    var = var+obs**2
    call glauber(s)
end do
med = med/N
var = (var-N*med**2)/(N-1)
print "((A20),*(f20.16))", "Glauber", med, sqrt(var/N) 

! Random Glauber
med = 0
var = 0
call hot_start(s)
do i=1, thermalization
    call random_glauber(s)
end do
do i=1, N
    obs = system_charge(s)**2
    med = med+obs
    var = var+obs**2
    call random_glauber(s)
end do
med = med/N
var = (var-N*med**2)/(N-1)
print "((A20),*(f20.16))", "Random Glauber", med, sqrt(var/N) 

! Cluster
med = 0
var = 0
call hot_start(s)
do i=1, thermalization
    call cluster(s)
end do
do i=1, N
    obs = system_charge(s)**2
    med = med+obs
    var = var+obs**2
    call cluster(s)
end do
med = med/N
var = (var-N*med**2)/(N-1)
print "((A20),*(f20.16))", "Cluster", med, sqrt(var/N) 

end program
