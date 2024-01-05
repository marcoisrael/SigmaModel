program cooling
    use algorithm
    use functions
    real(8), allocatable :: s(:,:),s0(:,:), med(:,:), var(:,:), interval(:)
    real(8), dimension(2) :: obs
    real(8) ::  startTemp, endTemp
    integer :: N, thermalization, TQ, i, k
    character(30), dimension(8) :: arg
    character(60) :: path
    call get_command_argument(1,arg(1))   
    call get_command_argument(2,arg(2))  
    call get_command_argument(3,arg(3))   
    call get_command_argument(4,arg(4))   
    call get_command_argument(5,arg(5))   
    call get_command_argument(6,arg(6))
    call get_command_argument(7,arg(7))      
    arg(8) = "multi"
    LENGTH = 64
    VOLUME = LENGTH*LENGTH
    thermalization = 2e3
    startTemp = string2real(arg(1))
    endTemp = string2real(arg(2))
    TQ = string2int(arg(3))
    N = string2int(arg(4))
    allocate(s(VOLUME,3), s0(VOLUME,3))
    allocate(interval(0:TQ), med(0:TQ,2), var(0:TQ,2))
    med(:,:)=0
    var(:,:)=0
    temp = startTemp
    beta = 1/startTemp
    interval = linspace(startTemp, endTemp, TQ)
    call hot_start(s0)
    do i=1, thermalization
        call cluster(s0, arg(8))
    end do
    do i=1, N
        temp = startTemp
        beta = 1/startTemp
        s = s0
        do k=1, 50
            call cluster(s, arg(8))
        end do
        s0 = s
        do k=0, TQ
            temp = interval(k)
            beta = 1/temp
            call step(s, arg(6), arg(7))
            obs = [system_charge(s)**2/VOLUME,control_param]
            med(k,:)=med(k,:)+obs
            var(k,:)=var(k,:)+obs(:)*obs(:)
        end do
    end do
    med(:,:)=med(:,:)/N
    var(:,:)=(var(:,:)-N*med(:,:)**2)/(N-1)
    path = trim(arg(5))//trim(arg(6))//"_"//trim(arg(7))//" "//trim(arg(3))//".csv"
    open(unit=1, file=path)
    write(1, '(*(g0,:,","))') 'tau_Q', 'T', 'chi_t', 'Error chi_t','AR|CS','Error AR|CS'
    do k=0,TQ
        write(1, '((I0,:,","),*(f0.16,:,","))') k, interval(k), med(k,1) , &
        sqrt(var(k,1)/N), med(k,2), sqrt(var(k,2)/N)
    end do
end program
