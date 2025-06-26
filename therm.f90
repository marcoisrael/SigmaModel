program therm
   use algorithm
   use functions
   real(8), allocatable :: s(:,:), med(:,:,:), x(:,:,:), interval(:), medjk(:,:), varjk(:,:)
   real(8) :: obs(2)
   real(8) ::  startTemp, endTemp
   integer :: N, sample,thermalization, TQ, i, j, k, l
   character(60), dimension(10) :: arg
   character(60) :: path
   call get_command_argument(1,arg(1))
   call get_command_argument(2,arg(2))
   call get_command_argument(3,arg(3))
   call get_command_argument(4,arg(4))
   call get_command_argument(5,arg(5))
   call get_command_argument(6,arg(6))
   call get_command_argument(7,arg(7))
   call get_command_argument(8,arg(8))
   call get_command_argument(9,arg(9))
   arg(10) = "multi"
   LENGTH = string2int(arg(9))
   VOLUME = LENGTH*LENGTH
   thermalization = 1e4
   startTemp = string2real(arg(1))
   endTemp = string2real(arg(2))
   TQ = string2int(arg(3))
   N = string2int(arg(4))

   delta_step = string2real(arg(8))
   sample = N/100
   allocate(s(VOLUME,3))
   allocate(interval(0:TQ), med(100,0:TQ,2))
   allocate(x(100,0:TQ,2), medjk(0:TQ,2), varjk(0:TQ,2))
   med(:,:,:)=0
   temp = startTemp
   beta = 1/startTemp
   interval = linspace(startTemp, endTemp, TQ)
   call hot_start(s)
   do i=1, thermalization
      call cluster(s, arg(10))
   end do
   do k=0, TQ
      temp = interval(k)
      beta = 1/temp
      delta_step = dmin1(0.08419342-0.21964047*temp+0.3387236*temp*temp, dble(1))
      do j=1, 100
         do i=1, sample
            call cluster(s, arg(10))
            obs = [system_charge(s)**2,control_param]
            obs = obs/VOLUME
            med(j,k,:)=med(j,k,:)+obs
         end do
      end do
      do i=1, 100
         call cluster(s, arg(9))
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
   path = trim(arg(5))//"/"//trim(arg(1))//"-"//trim(arg(2))//"-"//trim(arg(3))//".csv"
   open(unit=1, file=path)
   write(1, '(*(g0,:,","))') 'tau_Q', 'T', 'chi_t', 'Error chi_t','AR|CS','Error AR|CS'
   do k=0,TQ
      write(1, '((I0,:,","),*(f0.16,:,","))') k, interval(k), medjk(k,1) , &
         varjk(k,1), medjk(k,2), varjk(k,2)
   end do ! hola xd
end program
