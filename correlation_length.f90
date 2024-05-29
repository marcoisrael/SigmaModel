program measure
    use algorithm
    use functions
    real(8), allocatable :: s(:,:), cl(:,:)
    real(8), allocatable :: obs(:), med(:), var(:)
    integer :: N, thermalization, i, j, k, sp
    character(30) ::  str1="multi"
    character(30), dimension(7) :: arg 
    character(60) :: path
    call get_command_argument(1,arg(1))
    call get_command_argument(2,arg(2))  
    call get_command_argument(3,arg(3)) 
    call get_command_argument(4,arg(4))  
    call get_command_argument(5,arg(5))  
    call get_command_argument(6,arg(6))
    call get_command_argument(7,arg(7))
   
    LENGTH = string2int(arg(7))
    VOLUME = LENGTH*LENGTH
    thermalization = 1e4
    Temp = string2real(arg(1))
    delta_step = string2real(arg(5))
    N = string2int(arg(2))
    sp = 12 !ceiling(915.43*exp(-temp/0.1644))
    delta_step = dmin1(0.08419342-0.21964047*temp+0.3387236*temp*temp, dble(1))

    allocate(s(VOLUME,3),cl(VOLUME,3))
    allocate(obs(VOLUME), med(VOLUME), var(VOLUME))
    call hot_start(s)

    beta = 1/Temp

    do k=1, thermalization
        call cluster(s, str1)
    end do
    
    do k=1, N
        do i=1, sp
            call step(s, arg(3), arg(4))
        end do
        cl(:,:) = 0
        do i=1, LENGTH
            do j=1, LENGTH
                cl(i,:) = cl(i,:)+s(getindex(i,j),:)
            end do
            cl(i,:) = cl(i,:)/LENGTH
            obs(i) = dot_product(cl(1,:),cl(i,:))
            med(i) = med(i)+obs(i)
            var(i) = var(i)+obs(i)*obs(i)
        end do
    end do 
    
    med = med/N
    var = var/N
    var = sqrt(var-med*med)/sqrt(dble(N))
    path = 'output/correlation_length/L'//trim(int2string(LENGTH))&
            //"/"//trim(arg(3))//"_"//trim(arg(4))//'/'//trim(arg(1))//".csv"

    open(unit=1, file=path)
    write(1, '(*(g0,:,","))') "i", "correlation_length", "error"

    do i=1, LENGTH
        write(1, '(*(g0,:,","))') i-1, med(i), var(i)
    end do
    write(1, '(*(g0,:,","))') LENGTH, med(1), var(1)
end program
