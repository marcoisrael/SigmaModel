program cooling
   use algorithm
   use functions
   real(8), allocatable :: s(:,:),s0(:,:), med(:,:),var(:,:), rangeTemp(:)
   real(8) :: obs(3)
   real(8) ::  startTemp, endTemp
   integer :: N,thermalization, TQ, i, j, k
   character(30), dimension(9) :: arg
   character(60) :: path
   call get_command_argument(1,arg(1))
   call get_command_argument(2,arg(2))
   call get_command_argument(3,arg(3))
   call get_command_argument(4,arg(4))
   call get_command_argument(5,arg(5))
   call get_command_argument(6,arg(6))
   call get_command_argument(7,arg(7))
   call get_command_argument(8,arg(8))
   arg(9) = "multi"
   LENGTH = 64
   VOLUME = LENGTH*LENGTH
   thermalization = 1e4
   startTemp = string2real(arg(1))
   endTemp = string2real(arg(2))
   TQ = string2int(arg(3))
   N = string2int(arg(4))
   delta_step = string2real(arg(8))
   allocate(s(VOLUME,3), s0(VOLUME,3))
   allocate(rangeTemp(0:TQ), med(0:TQ,3),var(0:TQ,3))
   med(:,:)=0
   var(:,:)=0
   temp = startTemp
   beta = 1/startTemp
   rangeTemp = linspace(startTemp, endTemp, TQ)
   call hot_start(s0)
   do i=1, thermalization
      call cluster(s0, arg(9))
   end do
   do i=1, N
      temp = startTemp
      beta = 1/startTemp
      s = s0
      do k=1, 10
         call cluster(s, arg(9))
      end do
      s0 = s
      do k=0, TQ
         temp = rangeTemp(k)
         beta = 1/temp
         call step(s, arg(6), arg(7))
         obs = [system_charge(s)**2, system_energy(s), system_magnetization(s)]
         obs = obs/VOLUME
         med(k,:)=med(k,:)+obs
         var(k,:)=var(k,:)+obs**2
      end do
   end do

   med = med/N
   var = var/N
   var = sqrt(var-med*med)/sqrt(dble(N))

   path = trim(arg(5))//"/"//trim(arg(6))//"_"//trim(arg(7))//" "//trim(arg(3))//".csv"

   open(unit=1, file=path)
   write(1, '(*(g0,:,","))') 'tau_cool', 'temp', 'chi_t', 'error_chi_t', &
      'energy_density', 'error_energy_density', 'magnetization', 'error_magnetization'
   do k=0,TQ
      write(1, '((I0,:,","),*(f0.16,:,","))') k, rangeTemp(k), med(k,1) , &
         var(k,1), med(k,2), var(k,2), med(k,3), var(k,3)
   end do
end program
