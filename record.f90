program record
    use algorithm
    use functions
    real(8), allocatable :: s(:, :)
    real(8), dimension(3) :: obs
    integer :: n, steps, thermalization, i, j, sp
    character(30) :: arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, str1 = "multi"
    character(90) :: path,name
    call get_command_argument(1, arg1)
    call get_command_argument(2, arg2)
    call get_command_argument(3, arg3)
    call get_command_argument(4, arg4)
    call get_command_argument(5, arg5)
    call get_command_argument(6, arg6)
    call get_command_argument(7, arg7)
    call GET_COMMAND_ARGUMENT(8, arg8)
    length = string2int(arg6)
    volume = length * length
    thermalization = 1e4
    temp = string2real(arg1)
    n = string2int(arg2)
    sp = string2int(arg7)
    delta_step = dmin1(0.08419342 - 0.21964047 * temp + 0.3387236 * temp * temp, dble(1))
    allocate(s(volume, 3))

    call cold_start(s)
    path = "output/cold.csv"
    beta = 1 / temp

    ! do i = 1, thermalization
    !     call cluster(s, str1)
    ! end do
    ! path = 'output/' // trim(arg8) //'/L' // trim(arg6) // "/" // trim(arg3) // "_" // trim(arg4) // '/' // trim(arg1) // ".csv"
    open(unit = 1, file = path)
    write(1, '(*(g0,:,","))') 'H/V', 'chi_t', 'chi_m'

    do i = 1, n
        do j = 1, sp
            call step(s, arg3, arg4)
        end do
        obs = [system_energy(s), system_charge(s), system_magnetization(s)]
        obs(:) = obs(:) / volume
        write(1, '(*(f0.16,:,","))') obs
    end do
end program
