program main
use algorithm
use functions
use m_progress_bar
real(8), allocatable, dimension(:,:,:) :: s
real(8), allocatable, dimension(:,:) ::  Smp, medSmp
real(8), allocatable, dimension(:) :: interval
real(8) :: medJK, varJK, startTemp, endTemp
integer :: N, thermalization, packages, sizeJk, TQ, j,k
character(60) path
LENGTH = 8
VOLUME = LENGTH*LENGTH
thermalization = 30
startTemp = 4.
endTemp = 0. 
packages = 100
N = 1e5
TQ = 80

path = "output/susceptibility/80.tsv"
open(unit=1, file=path)
allocate(s(LENGTH,LENGTH,3))
allocate(interval(TQ), Smp(TQ,packages), medSmp(TQ,packages))
write(1, "((A4),*(A25))") 'TQ', 'Temp', 'susceptibility', 'error'

sizeJk = N/packages
Smp(:,:) = 0
medSmp(:,:) = 0
do i=1, packages
    do j=1, sizeJk
        interval = linspace(startTemp, endTemp, TQ)
        call hot_start(s)
        beta = 1/startTemp
        do k=1, thermalization
            call cluster(s)
        end do

        do k=1, TQ
            beta = 1/interval(k)
            call metropolis(s)
            Smp(k,i) = Smp(k,i)+system_charge(s)**2
        end do
    end do
    do k=1, TQ
        Smp(k,i) = Smp(k,i)/sizeJk
    end do
    call progress_bar(i, packages)
end do

do k=1, TQ
    medJK = 0
    varJK = 0
    do i=1, packages
        do j=1, packages
            if (i/=j) then
                medSmp(k,i) = medSmp(k,i)+Smp(k,j)
            end if
        end do
        medSmp(k,i) = medSmp(k,i)/(packages-1)
        medJK = medJK+medSmp(k,i)
    end do
    medJK = medJK/packages

    do i=1, packages
        varJK = varJK+(medSmp(k,i)-medJK)**2
    end do
    varJK = varJK*(packages-1)

    write(1, "((I4),*(f25.16))") k, interval(k), medJK, sqrt(varJK/packages)
end do

end program
