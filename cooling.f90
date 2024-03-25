program cooling
    use algorithm
    use functions
    real(8), allocatable :: s(:,:),s0(:,:), med(:,:,:), x(:,:,:), interval(:), medjk(:,:), varjk(:,:)
    real(8) :: obs(2)
    real(8) ::  startTemp, endTemp
    integer :: N, sample,thermalization, TQ, i, j, k
    character(30), dimension(8) :: arg
    character(60) :: path
    call get_command_argument(1,arg(1))   
    call get_command_argument(2,arg(2))  
    call get_command_argument(3,arg(3))   
    call get_command_argument(4,arg(4))   
    call get_command_argument(5,arg(5))   
    call get_command_argument(6,arg(6))
    call get_command_argument(7,arg(7))
    call get_command_argument(8,arg(8))          
    arg(8) = "multi"
    LENGTH = 64
    VOLUME = LENGTH*LENGTH
    thermalization = 1e4
    startTemp = string2real(arg(1))
    endTemp = string2real(arg(2))
    TQ = string2int(arg(3))
    N = string2int(arg(4))
    delta_step = string2real(arg(8))
    sample = N/100
    allocate(s(VOLUME,3), s0(VOLUME,3))
    allocate(interval(0:TQ), med(100,0:TQ,2))
    allocate(x(100,0:TQ,2), medjk(0:TQ,2), varjk(0:TQ,2))
    med(:,:,:)=0
    temp = startTemp
    beta = 1/startTemp
    interval = linspace(startTemp, endTemp, TQ)
    interval = 1/sqrt(interval)
    call hot_start(s0)
    do i=1, thermalization
        call cluster(s0, arg(8))
    end do
    do j=1, 100
		do i=1, sample 
			temp = startTemp
			beta = 1/startTemp
			s = s0
			do k=1, 10
				call cluster(s, arg(8))
			end do
			s0 = s
			do k=0, TQ
				temp = interval(k)
				beta = 1/temp
				call step(s, arg(6), arg(7))
				obs = [system_charge(s)**2/VOLUME,control_param]
				med(j,k,:)=med(j,k,:)+obs
			end do
		end do
    end do
    medjk(:,:) = 0
    varjk(:,:) = 0
    x(:,:,:) = 0
    med(:,:,:) = med(:,:,:)/sample
    do i=1, 100
		do j=1, 100
			if (i/=j) then
				x(i,:,:) = x(i,:,:)+med(j,:,:)
			end if
		end do
		x(i,:,:) = x(i,:,:)/99
		medjk(:,:) = medjk(:,:)+x(i,:,:)
    end do
    medjk(:,:)=medjk(:,:)/100
    do i=1, 100
		varjk(:,:)=varjk(:,:)+(x(i,:,:)-medjk(:,:))**2
	end do
	varjk(:,:) = sqrt(.99*varjk(:,:))
    path = trim(arg(5))//trim(arg(6))//"_"//trim(arg(7))//" "//trim(arg(3))//".csv"
    open(unit=1, file=path)
    write(1, '(*(g0,:,","))') 'tau_Q', 'T', 'chi_t', 'Error chi_t','AR|CS','Error AR|CS'
    do k=0,TQ
        write(1, '((I0,:,","),*(f0.16,:,","))') k, interval(k), medjk(k,1) , &
        varjk(k,1), medjk(k,2), varjk(k,2)
    end do
end program
