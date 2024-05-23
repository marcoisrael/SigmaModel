program record
    use algorithm
    use functions
    real(8), allocatable :: s(:,:)
    real(8), dimension(3) :: obs
    integer :: N, steps, thermalization, i, j, sp
    character(30) :: arg1, arg2, arg3, arg4, arg5, arg6, str1="multi"
    character(60) :: path
    call get_command_argument(1,arg1)   
    call get_command_argument(2,arg2)  
    call get_command_argument(3,arg3) 
    call get_command_argument(4,arg4)  
    call get_command_argument(5,arg5)
    call get_command_argument(6,arg6)
    LENGTH = 128
    VOLUME = LENGTH*LENGTH
    thermalization = 1e4
    Temp = string2real(arg1)
    delta_step = string2real(arg5)
    N = string2int(arg2)
    sp = string2int(arg6)
    allocate(s(VOLUME,3))
    call hot_start(s)
    beta = 1/Temp
    do i=1, thermalization
        call cluster(s, str1)
    end do
    path = 'output/record-1/L'//trim(int2string(LENGTH))//"/"//trim(arg3)//"_"//trim(arg4)//'/'//trim(arg1)//".csv"
    open(unit=1, file=path)
    write(1, '(*(g0,:,","))') 'H/V', 'chi_t', 'chi_m'
    do i=1, N
        do j=1, sp
            call step(s, arg3, arg4)
        end do
        obs = [system_energy(s), system_charge(s), system_magnetization(s)]
        obs(:) = obs(:)/VOLUME
        write(1, '(*(f0.16,:,","))') obs
    end do 
end program
