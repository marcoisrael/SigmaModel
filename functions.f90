module functions
    real(8) ::  pi=4.0*datan(1.0d0), beta, temp
    real(8), dimension(4) :: values 
    logical :: update_values=.false.
    integer :: LENGTH, VOLUME
    ! logical :: save
    contains

    subroutine hot_start(s)
        real(8), dimension(LENGTH,LENGTH) :: theta, phi, r
        real(8), dimension(LENGTH,LENGTH,3) :: s
        call random_number(r)
        call random_number(phi)
        theta = acos(1-2*r)
        phi = 2*pi*phi
        s(:,:, 1) = sin(theta)*cos(phi)
        s(:,:, 2) = sin(theta)*sin(phi)
        s(:,:, 3) = cos(theta)
    end subroutine

    function random()
        real(8) :: random
        call random_number(random)
    end function

    function random_vector()
        real(8),dimension(3) :: random_vector
        real(8) :: theta, phi
        theta = acos(1-2*random())
        phi = 2*pi*random()
        random_vector = [sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)]
    end function

    function modl(i)
        integer i, modL
        modl = modulo(i, LENGTH)
        if (modl==0) then
            modl = LENGTH
        end if
    end function

    function wolff_reflection(v, w)
        real(8), dimension(3) :: v, w, wolff_reflection
        wolff_reflection = v-2*dot_product(v, w)*w
    end function

    function cross_product(a, b)
        real(8), dimension(3) :: cross_product
        real(8), dimension(3) :: a, b
        cross_product(1) = a(2) * b(3) - a(3) * b(2)
        cross_product(2) = a(3) * b(1) - a(1) * b(3)
        cross_product(3) = a(1) * b(2) - a(2) * b(1)
    end function

    function system_charge(s)
        real(8), dimension(LENGTH,LENGTH,3) :: s
        real(8) system_charge, X1, Y1, X2, Y2
        real(8),dimension(3) :: e1, e2, e3, e4
        integer :: k=1
        system_charge = 0
        do i=1, LENGTH
            do j=1, LENGTH
                e1 = s(modl(i+1),j,:)
                e2 = s(modl(i+1),modl(j+1),:)
                e3 = s(i,j,:)
                e4 = s(i,modl(j+1),:)
                if (k>0) then    
                    X1 = 1+dot_product(e1,e2)+dot_product(e2,e3)+dot_product(e3,e1)
                    Y1 = dot_product(e1, cross_product(e2,e3))
                    X2 = 1+dot_product(e4,e3)+dot_product(e3,e2)+dot_product(e2,e4)
                    Y2 = dot_product(e4, cross_product(e3,e2))
                else 
                    X1 = 1+dot_product(e1,e2)+dot_product(e2,e4)+dot_product(e4,e1)
                    Y1 = dot_product(e1,cross_product(e2,e4))
                    X2 = 1+dot_product(e1,e4)+dot_product(e4,e3)+dot_product(e3,e1)
                    Y2 = dot_product(e1,cross_product(e4,e3))
                end if
                system_charge = system_charge+atan2(Y1,X1)+atan2(Y2,X2)
                k =-k
            end do
        end do
        system_charge=0.5*system_charge/pi
    end function

    function system_energy(s)
        real(8),dimension(LENGTH,LENGTH,3) :: s
        real(8), dimension(3) :: sx, sx_right, sx_down
        real(8) :: system_energy
        system_energy = 0
        do i=1, LENGTH
            do j=1, LENGTH
                sx = s(i,j,:)
                sx_right = s(modl(i+1),j,:)
                sx_down = s(i,modl(j+1),:)
                system_energy = system_energy-dot_product(sx,sx_right)-dot_product(sx,sx_down)
            end do
        end do
        system_energy = system_energy/VOLUME
    end function

    function is_bond(sx, sy, w)
        logical :: is_bond
        real(8), dimension(3) :: sx, sy, w
        real(8) :: delta, p
        delta = -dot_product(wolff_reflection(sx, w), sy)+dot_product(sx, sy)
        if (delta<=0) then
            p = 0
        else
            if (temp<=0.) then
                p = 1
            else 
                p = 1-exp(-beta*delta)
            end if
        end if
        if (random()<=p) then
            is_bond = .true.
        else
            is_bond = .false.
        end if
    end function

    subroutine join(group, label1, label2, largest_label)
        integer, dimension(LENGTH,LENGTH) :: group
        integer :: label1, label2, label_min, label_max
        if (label1/=label2) then
            if (label1<label2) then
                label_max = label2
                label_min = label1
            else
                label_max = label1
                label_min = label2
            end if
            do i=1, LENGTH
                do j=1, LENGTH
                    if (group(i,j)==label_max) then
                        group(i,j) = label_min
                    else if (group(i,j)>label_max) then
                        group(i,j) = group(i,j)-1
                    end if
                end do
            end do
            largest_label = largest_label-1
        end if
    end subroutine

    function int2string(i)
        character(30) :: style, int2string
        integer :: i
        if (i<100) then
            style = "(I3)"
        else if (i<10) then
            style = "(I2)"
        else
            style = '(I1)'
        end if
        write(int2string, style) i
    end function

    function string2int(string)
        character(30) :: string
        integer :: string2int
        read (string,'(I10)') string2int
    end function

    function string2real(string)
        character(30) :: string
        real(8) :: string2real
        read (string,*) string2real
    end function

    function random_integer(i)
        real r
        integer i, random_integer
        call random_number(r)
        random_integer = ceiling(i*r)
    end function

    function linspace(a, b, n)
        integer n, i
        real(8), dimension(0:n) :: linspace
        real(8) a, b
        do i=0, n
            linspace(i) = a+(b-a)*i/n
        end do
    end function
end module