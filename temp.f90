program cooling
    use algorithm
    use functions
    real(8), allocatable, dimension(:,:,:) :: s
    real(8), allocatable, dimension(:,:) :: Smp, medSmp
    real(8), dimension(2) :: medJK, varJK
    integer :: N, thermalization, packages, sizeJk, i, j
    character(30) arg1, arg2, arg3, arg4
    call get_command_argument(1,arg1)   
    call get_command_argument(2,arg2)  
    call get_command_argument(3,arg3) 
    call get_command_argument(4,arg4)  
 
   
    LENGTH = 8
    VOLUME = LENGTH*LENGTH
    thermalization = 100
    Temp = string2real(arg1)
    N = string2int(arg2)
    packages = 25
    allocate(s(LENGTH,LENGTH,3))
    allocate(Smp(2,packages), medSmp(2,packages))

    sizeJk = N/packages
    Smp(:,:) = 0
    medSmp(:,:) = 0
    x = 0
    call hot_start(s)
    beta = 1/Temp
    do i=1, thermalization
        call cluster(s, arg3)
    end do
    do i=1, packages
        do j=1, sizeJk
            call step(s, arg3, arg4)
            Smp(1,i) = Smp(1,i)+system_energy(s)
            Smp(2,i) = Smp(2,i)+system_charge(s)**2
        end do
    end do
    Smp(:,:)= Smp(:,:)/sizeJk

    medJK(:) = 0
    varJK(:) = 0
    do i=1, packages
        do j=1, packages
            if (i/=j) then
                medSmp(:,i) = medSmp(:,i)+Smp(:,j)
            end if
        end do
        medSmp(:,i) = medSmp(:,i)/(packages-1)
        medJK(:) = medJK(:)+medSmp(:,i)
    end do
    medJK(:) = medJK(:)/packages

    do i=1, packages
        varJK(:) = varJK(:)+(medSmp(:,i)-medJK(:))**2
    end do
    varJK(:) = varJK(:)*(packages-1)
    print "(A25,*(f25.16))", 'energy density',medJK(1), sqrt(varJK(1)/packages)
    print "(A25,*(f25.16))", 'topoligical charge',medJK(2), sqrt(varJK(2)/packages)
end program
