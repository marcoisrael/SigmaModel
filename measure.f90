program measure
    use algorithm
    use functions
    real(8), allocatable :: s(:,:)
    real(8), dimension(4) :: obs, med, var
    integer :: N, steps, thermalization, i, j
    character(30) :: arg1, arg2, arg3, arg4, str1="multi"
    character(60) :: path
    call get_command_argument(1,arg1)   
    call get_command_argument(2,arg2)  
    call get_command_argument(3,arg3) 
    call get_command_argument(4,arg4)  
   
    LENGTH = 64
    VOLUME = LENGTH*LENGTH
    thermalization = 1e3
    Temp = string2real(arg1)
    steps = string2int(arg2)
    N = steps
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
    
    var(:) = (var(:)-N*med(:)*med(:))/(N-1)
    print*, med
    print*, sqrt(var/N)
end program
