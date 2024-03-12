module algorithm
    use functions
    contains

    subroutine hoshen_kopelman(labels, bond, i, j, largest_label)
        integer ::  largest_label, bond(VOLUME,2)
        type(labelType) :: labels(VOLUME)
        i1 = modl(i+1)
        j1 = modl(j+1)
        if (bond(getindex(i,j),1)==0) then
            if (bond(getindex(i,j),2)==0) then
                largest_label = largest_label+1
                bond(getindex(i,j),2) = largest_label
                largest_label = largest_label
                labels(largest_label)%cluster = [getindex(i,j)]
            end if
        else if (bond(getindex(i,j),1)==10) then
            call join([i, j],[i1, j], largest_label, labels, bond)
        else if (bond(getindex(i,j),1)==1) then
            call join([i, j],[i, j1], largest_label, labels, bond)
        else if (bond(getindex(i,j),1)==11) then
            call join([i, j],[i1, j], largest_label, labels, bond)
            call join([i, j],[i, j1], largest_label, labels, bond)
        end if
    end subroutine

    subroutine cluster(s, key)
        real(8), allocatable :: s(:,:)
        real(8), dimension(3) :: sx, right, down, w
        integer :: largest_label, bond(VOLUME,2), k
        character(30) :: key
        type(labelType) :: labels(VOLUME)
        w = random_vector()
        largest_label = 0
        bond(:,:) = 0 
        do i=1, LENGTH
            do j=1, LENGTH
                labels(getindex(i,j))%cluster = [0]
                sx = s(getindex(i,j),:)
                right = s(getindex(modl(i+1),j),:)
                down = s(getindex(i,modl(j+1)),:)
                if (is_bond(sx,right,w)) then
                    bond(getindex(i,j),1) = 10
                end if
                if (is_bond(sx,down,w)) then
                    bond(getindex(i,j),1) = bond(getindex(i,j),1)+1
                end if
                call hoshen_kopelman(labels, bond, i,j, largest_label)
            end do
        end do
		
        ! do i=1, LENGTH
        !    do j=1, LENGTH
        !        write(1, '(*(I0,:,","))') i, j, bond(getindex(i,j),1), bond(getindex(i,j),2)
        !    end do
        ! end do
        
        if (key=='single') then
            k = random_integer(largest_label) 
            do j=1, size(labels(k)%cluster)
                s(labels(k)%cluster(j),:) = s(labels(k)%cluster(j),:)&
                -2*dot_product(s(labels(k)%cluster(j),:),w)*w
            end do
        else if (key=='multi') then
            do i=1, largest_label
                if (random()<=0.5) then
                    do j=1, size(labels(i)%cluster)
                        s(labels(i)%cluster(j),:) = s(labels(i)%cluster(j),:)&
                        -2*dot_product(s(labels(i)%cluster(j),:),w)*w
                    end do
                end if
            end do
        end if
        control_param=dble(VOLUME)/largest_label
    end subroutine

    subroutine metropolis(s, key)
        real(8), allocatable :: s(:,:)
        real(8), dimension(3) :: sx, right, down, left, up, r
        real(8) :: h1, h2, delta, p, ar
        integer :: i, j, i1 , j1
        character(30) :: key
        ar=0
        do i1=1, LENGTH
            do j1=1, LENGTH
                if (key=='random') then
                    i = random_integer(LENGTH)
                    j = random_integer(LENGTH)
                else if (key=='lexic') then
                    i = i1
                    j = j1
                end if
                sx = s(getindex(i,j),:)
                right = s(getindex(modl(i+1),j),:)
                down = s(getindex(i,modl(j+1)),:)
                left = s(getindex(modl(i-1),j),:)
                up = s(getindex(i,modl(j-1)),:)
                r = random_vector_cone(sx)
                h1 = -dot_product(sx, right)-dot_product(sx, down) &
                    -dot_product(sx,left)-dot_product(sx,up)
                h2 = -dot_product(r, right)-dot_product(r, down) &
                    -dot_product(r,left)-dot_product(r,up)
                delta = h2-h1
                if (delta<=0) then
                    p = 1
                else
                    p = exp(-beta*delta)
                end if
                ar = ar+p
                if (random()<=p) then
                    s(getindex(i,j),:) = r
                end if
            end do
        end do
        control_param = ar
    end subroutine

    subroutine glauber(s, key)
        real(8), allocatable :: s(:,:)
        real(8), dimension(3) :: sx, right, down, left, up, r
        real(8) :: h1, h2, delta, p, ar
        integer :: i, j, i1 , j1
        character(30) :: key
        ar=0
        do i1=1, LENGTH
            do j1=1, LENGTH
                if (key=='random') then
                    i = random_integer(LENGTH)
                    j = random_integer(LENGTH)
                else if (key=='lexic') then
                    i = i1
                    j = j1
                end if
                sx = s(getindex(i,j),:)
                right = s(getindex(modl(i+1),j),:)
                down = s(getindex(i,modl(j+1)),:)
                left = s(getindex(modl(i-1),j),:)
                up = s(getindex(i,modl(j-1)),:)
                r = random_vector_cone(sx)
                h1 = -dot_product(sx, right)-dot_product(sx, down) &
                    -dot_product(sx,left)-dot_product(sx,up)
                h2 = -dot_product(r, right)-dot_product(r, down) &
                    -dot_product(r,left)-dot_product(r,up)
                delta = h2-h1
                if (temp==0.) then
                    if (delta>0) then
                        p = 0
                    else
                        p = 1
                    end if
                else
                    p = exp(-beta*delta)/(1+exp(-beta*delta))
                end if
                ar = ar+p
                if (random()<=p) then
                    s(getindex(i,j),:) = r
                end if
            end do
        end do
        control_param=ar/VOLUME
    end subroutine

    subroutine step(s, key, alg)
        real(8), allocatable :: s(:,:)
        character(30) :: alg, key
        if (alg=="metropolis") then
            call metropolis(s, key)
        else if (alg=="glauber") then
            call glauber(s, key)
        else if (alg=="cluster") then
            call cluster(s, key)
        end if
    end subroutine
end module
