module functions

    type :: labelType
        integer, allocatable :: cluster(:)
    end type labelType

    real(8) ::  pi=4.0*datan(1.0d0), beta, temp, control_param
    real(8), dimension(4) :: values 
    logical :: update_values=.false.
    integer :: LENGTH, VOLUME
    contains
    function getindex(i, j)
        integer i, j, getindex
        getindex = j+(i-1)*LENGTH
    end function
    subroutine join(x, y, largest_label, labels, bond)
        integer :: x(2), y(2), index,largest_label, m, n, i, bond(VOLUME,2)
        type(labelType) :: labels(VOLUME)
        n = bond(getindex(x(1),x(2)), 2)
        m = bond(getindex(y(1),y(2)), 2)
        if (n==0 .and. m==0) then
            largest_label = largest_label+1
            index = largest_label
            labels(index)%cluster = [getindex(x(1),x(2)), getindex(y(1),y(2))]
        else if (n>0 .and. m==0) then
            index = n
            labels(n)%cluster = [labels(n)%cluster, getindex(y(1),y(2))]
        else if (n==0 .and. m>0) then
            index = m
            labels(m)%cluster = [labels(m)%cluster, getindex(x(1),x(2))]
        else if (n/=m) then
            index = min(m,n)
            labels(index)%cluster = [labels(m)%cluster, labels(n)%cluster]
            if (max(m,n)<VOLUME) then
                do i=max(m,n), largest_label-1
                    labels(i)%cluster = labels(i+1)%cluster
                    bond(labels(i)%cluster,2) = i
                end do
            end if
            largest_label = largest_label-1
        end if
        bond(labels(index)%cluster,2) = index
    end subroutine 

    subroutine hot_start(s)
        real(8), dimension(VOLUME) :: theta, phi, r
        real(8), allocatable :: s(:,:)
        call random_number(r)
        call random_number(phi)
        theta = acos(1-2*r)
        phi = 2*pi*phi
        s(:, 1) = sin(theta)*cos(phi)
        s(:, 2) = sin(theta)*sin(phi)
        s(:, 3) = cos(theta)
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

    function random_vector_cone(v)
        real(8), dimension(3) :: random_vector_cone, r, k, v
        real(8) :: delta, phi
        r = random_vector()
        k = cross_product(r, v)
        delta = 1
        phi = sqrt(delta*random())
        random_vector_cone = v*cos(phi)+cross_product(k, v)*sin(phi)+k*dot_product(k, v)*(1-cos(phi))
        random_vector_cone = random_vector_cone/sqrt(dot_product(random_vector_cone, random_vector_cone))
    end function

    function modl(i)
        integer modL
        modl = modulo(i, LENGTH)
        if (modl==0) then
            modl = LENGTH
        end if
    end function

    function cross_product(a, b)
        real(8), dimension(3) :: cross_product
        real(8), dimension(3) :: a, b
        cross_product(1) = a(2) * b(3) - a(3) * b(2)
        cross_product(2) = a(3) * b(1) - a(1) * b(3)
        cross_product(3) = a(1) * b(2) - a(2) * b(1)
    end function

    function system_charge(s)
        real(8), allocatable :: s(:,:)
        real(8) system_charge, X1, Y1, X2, Y2
        real(8),dimension(3) :: e1, e2, e3, e4
        integer :: k=1
        system_charge = 0
        do i=1, LENGTH
            do j=1, LENGTH
                e1 = s(getindex(i,modl(j+1)),:)
                e2 = s(getindex(modl(i+1),modl(j+1)),:)
                e3 = s(getindex(i,j),:)
                e4 = s(getindex(modl(i+1),j),:)
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
        real(8), allocatable :: s(:,:)
        real(8), dimension(3) :: sx, right, down
        real(8) :: system_energy
        system_energy = 0
        do i=1, LENGTH
            do j=1, LENGTH
                sx = s(getindex(i,j),:)
                right = s(getindex(modl(i+1),j),:)
                down = s(getindex(i,modl(j+1)),:)
                system_energy = system_energy-dot_product(sx,right)-dot_product(sx,down)
            end do
        end do
    end function

    function system_magnetization(s)
        real(8), allocatable :: s(:,:)
        real(8), dimension(3) :: M
        real(8) :: system_magnetization
        system_magnetization = 0
        M(:) =  0
        do i=1, LENGTH
            do j=1, LENGTH
                M = M + s(getindex(i,j),:)
            end do
        end do
        system_magnetization = sqrt(dot_product(M,M))
    end function

    function is_bond(ex, ey, w)
        logical :: is_bond
        real(8), dimension(3) :: ex, ey, w
        real(8) :: delta
        delta = -dot_product(ex-2*dot_product(ex, w)*w, ey)+dot_product(ex, ey)
        if (delta<=0) then 
            is_bond=.false.
        else
            if (random()<1-exp(-beta*delta)) then
                is_bond=.true.
            else 
                is_bond=.false.
            end if
        end if
    end function

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
        random_integer = 1+floor(i*r)
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