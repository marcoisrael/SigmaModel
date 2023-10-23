program cooling
    use algorithm
    use functions
    ! use m_progress_bar
    real(8), allocatable, dimension(:,:,:) :: s, Smp, medSmp
    real(8), allocatable, dimension(:) :: interval
    real(8), dimension(2) :: medJK, varJK
    real(8) ::  startTemp, endTemp, x
    integer :: N, thermalization, packages, sizeJk, TQ, i, j, k
    character(60)  :: path
    character(30) :: arg1, arg2, arg3, arg4, arg5, arg6, arg7, str1="multi"
    call get_command_argument(1,arg1)   
    call get_command_argument(2,arg2)  
    call get_command_argument(3,arg3)   
    call get_command_argument(4,arg4)   
    call get_command_argument(5,arg5)   
    call get_command_argument(6,arg6)
    call get_command_argument(7,arg7)      

    LENGTH = 8
    VOLUME = LENGTH*LENGTH
    thermalization = 100
    startTemp = string2real(arg1)
    endTemp = string2real(arg2)
    packages = 10
    TQ = string2int(arg3)
    N = string2int(arg4)
    path = trim(arg5)//trim(arg6)//"_"//trim(arg7)//" "//trim(arg3)//".tsv"
    open(unit=1, file=path)
    allocate(s(LENGTH,LENGTH,3))
    allocate(interval(0:TQ), Smp(2,0:TQ,packages), medSmp(2,0:TQ,packages))
    write(1, "((A4),*(A25))") 'TQ', 'Temp', 'charge', 'error', 'chargeAbs', 'error'
    sizeJk = N/packages
    Smp(:,:,:) = 0
    medSmp(:,:,:) = 0
    do i=1, packages
        do j=1, sizeJk
            interval = linspace(startTemp, endTemp, TQ)
            call hot_start(s)
            temp = interval(0)
            beta = 1/temp
            do k=1, thermalization
                call cluster(s, str1)
            end do

            do k=0, TQ
                temp = interval(k)
                beta = 1/temp
                call step(s, arg6, arg7)
                x = system_charge(s)
                Smp(1,k,i) = Smp(1,k,i)+x**2
                Smp(2,k,i) = Smp(2,k,i)+abs(x)
            end do
        end do
        ! call progress_bar(i, packages)
    end do
    Smp(:,:,:)= Smp(:,:,:)/sizeJk

    do k=0, TQ
        medJK(:) = 0
        varJK(:) = 0
        do i=1, packages
            do j=1, packages
                if (i/=j) then
                    medSmp(:,k,i) = medSmp(:,k,i)+Smp(:,k,j)
                end if
            end do
            medSmp(:,k,i) = medSmp(:,k,i)/(packages-1)
            medJK(:) = medJK+medSmp(:,k,i)
        end do
        medJK(:) = medJK(:)/packages

        do i=1, packages
            varJK(:) = varJK(:)+(medSmp(:,k,i)-medJK)**2
        end do
        varJK(:) = varJK(:)*(packages-1)

        write(1, "((I4),*(f25.16))") k, interval(k), medJK(1), sqrt(varJK(1)/packages),medJK(2), sqrt(varJK(2)/packages)
    end do
end program
