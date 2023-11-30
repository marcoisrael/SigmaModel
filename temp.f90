program cooling
    use algorithm
    use functions
    real(8), allocatable :: s(:,:)
    real(8), dimension(3) :: med, var, obs
    integer :: N, steps, thermalization, spacing, i, j
    character(30) :: arg1, arg2, arg3, arg4, str1="multi"
    call get_command_argument(1,arg1)   
    call get_command_argument(2,arg2)  
    call get_command_argument(3,arg3) 
    call get_command_argument(4,arg4)  
   
    LENGTH = 64
    VOLUME = LENGTH*LENGTH
    thermalization = 100
    Temp = string2real(arg1)
    steps = string2int(arg2)
    spacing = 10
    N = int(steps/spacing)
    allocate(s(VOLUME,3))
    call hot_start(s)

    beta = 1/Temp
    do i=1, thermalization
        call step(s, arg3, arg4)
    end do

    do i=1, N
        do j=1, spacing
            call step(s, arg3, arg4)
        end do
        obs = [system_energy(s), system_charge(s)**2/VOLUME, control_param]
        med = med+obs
        var(:) = var(:)+obs(:)**2 
    end do 
    med(:) = med(:)/N
    var(:) = (var(:)-N*med(:)**2)/(N-1)
    print "(A25,*(f25.16))", 'energy density',med(1), sqrt(var(1)/N)
    print "(A25,*(f25.16))", 'topoligical charge',med(2), sqrt(var(2)/N)
    print "(A25,*(f25.16))", 'control parameter',med(3), sqrt(var(3)/N)

end program
