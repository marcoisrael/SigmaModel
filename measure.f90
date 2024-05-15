program measure
    use algorithm
    use functions
    real(8), allocatable :: s(:,:)
    real(8), dimension(4) :: obs, med, var
    integer :: N, thermalization, i, j
    character(30) :: arg1, arg2, arg3, arg4, arg5, str1="multi"
    character(60) :: path
    call get_command_argument(1,arg1)   
    call get_command_argument(2,arg2)  
    call get_command_argument(3,arg3) 
    call get_command_argument(4,arg4)  
    call get_command_argument(5,arg5)  

   
    LENGTH = 64
    VOLUME = LENGTH*LENGTH
    thermalization = 1e4
    Temp = string2real(arg1)
    delta_step = string2real(arg5)
    N = string2int(arg2)
    allocate(s(VOLUME,3))
    call hot_start(s)

    var(:) = 0 
    obs(:) = 0
    beta = 1/Temp

    do i=1, thermalization
        call cluster(s, str1)
    end do
    
    do i=1, N
        call step(s, arg3, arg4)
        obs = [system_energy(s), system_charge(s)**2, system_magnetization(s), control_param]
        obs = obs/VOLUME
        med = med+obs
        var(:) = var(:)+obs(:)*obs(:)
    end do 
    
    med = med/N
    var = var/N
    var = sqrt(var-med*med)
    print*, med
    print*, var/sqrt(dble(N))
end program
