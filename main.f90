program main
use algorithm
use functions
real(8), allocatable, dimension(:,:,:) :: s
real(8), allocatable, dimension(:) ::  Smp, medSmp, serie
real(8) :: temperature, medJK, varJK
integer :: N, thermalization, packages, sizeJk
! character(60) path
LENGTH = 8
VOLUME = LENGTH*LENGTH
thermalization = 30
temperature = 4.
beta = 1/temperature
N = 1e3
packages = 100
allocate(s(LENGTH,LENGTH,3), Smp(packages), medSmp(packages), serie(N))


call hot_start(s)
do i=1, thermalization
    call cluster(s)
end do

sizeJk = N/packages
medSmp(:) = 0

do i=1, packages
    do j=1, sizeJk
        Smp(i) = Smp(i)+system_charge(s)**2
        call metropolis(s)
    end do
    Smp(i) = Smp(i)/sizeJk
end do

medJK = 0
varJK = 0

do i=1, packages
    do j=1, packages
        if (i/=j) then
            medSmp(i) = medSmp(i)+Smp(j)
        end if
    end do
    medSmp(i) = medSmp(i)/(packages-1)
    medJK = medJK+medSmp(i)
end do
medJK = medJK/packages

do i=1, packages
    varJK = varJK+(medSmp(i)-medJK)**2
end do
varJK = varJK*(packages-1)

print "((A20),*(f25.16))", "Metropolis", medJK, sqrt(varJK/packages)


end program
