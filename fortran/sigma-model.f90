program xymodel
use method
use functions
!use m_progress_bar
real(8), allocatable, dimension(:,:,:) :: s
real(8), dimension(64,3) :: configs
! real(8) :: temperature
! integer :: N, thermalization, cycles
! character(60) path
LENGTH = 8
! VOLUME = LENGTH*LENGTH
! thermalization = 1e2
! temperature = 4
! beta = 1/temperature
! cycles = 1e4
! N = 1000
allocate(s(LENGTH,LENGTH,3))
open(unit=1,file='configurations/config_1.csv')
do i=1, 64
    read(1, *) configs(i,:)
end do

do i=1, LENGTH
    do j=1,LENGTH
        s(i,j,:) = configs((i-1)*8+j,:)
        print*, s(i,j,:)
    end do
end do


end program