module algorithm
    use functions
    contains

    subroutine hoshen_kopelman(group, bond, i, j, largest_label)
        integer, dimension(LENGTH,LENGTH) :: group, bond
        integer ::  largest_label
        i1 = modl(i+1)
        j1 = modl(j+1)
        if (group(i,j)==0) then
            if (bond(i,j)==0) then
                largest_label =largest_label+1
                group(i,j) = largest_label
            else if (bond(i,j)==10) then
                if (group(i1,j)==0) then
                    largest_label =largest_label+1
                    group(i,j) = largest_label
                    group(i1,j) = group(i,j)
                else
                    group(i,j) = group(i1,j)
                end if
            else if (bond(i,j)==1) then
                if (group(i,j1)==0) then
                    largest_label =largest_label+1
                    group(i,j) = largest_label
                    group(i,j1) = group(i,j)
                else
                    group(i,j) = group(i,j1)
                end if     
            else if (bond(i,j)==11) then
                if ((group(i1,j)==0).and.(group(i,j1)==0)) then
                    largest_label =largest_label+1
                    group(i,j) = largest_label
                    group(i1,j) = group(i,j)
                    group(i,j1) = group(i,j)
                else if ((group(i1,j)>0).and.(group(i,j1)==0)) then
                    group(i,j) = group(i1,j)
                    group(i,j1) = group(i1,j)
                else if ((group(i1,j)==0).and.(group(i,j1)>0)) then
                    group(i,j) = group(i,j1)
                    group(i1,j) = group(i,j1)
                else
                    call join(group, group(i1,j),group(i,j1), largest_label)
                    group(i,j) = group(i1,j)
                end if
            end if
        else
            if (bond(i,j)==10) then
                if (group(i1,j)==0) then
                    group(i1,j) = group(i,j)
                else
                    call join(group, group(i,j),group(i1,j), largest_label)
                end if
            else if (bond(i,j)==1) then
                if (group(i,j1)==0) then
                    group(i,j1) = group(i,j)
                else
                    call join(group, group(i,j),group(i,j1), largest_label)
                end if     
            else if (bond(i,j)==11) then
                if ((group(i1,j)==0).and.(group(i,j1)==0)) then
                    group(i1,j) = group(i,j)
                    group(i,j1) = group(i,j)
                else if ((group(i1,j)>0).and.(group(i,j1)==0)) then
                    call join(group, group(i,j),group(i1,j), largest_label)
                    group(i,j1) = group(i,j)
                else if ((group(i1,j)==0).and.(group(i,j1)>0)) then
                    call join(group, group(i,j),group(i,j1), largest_label)
                    group(i1,j) = group(i,j)
                else
                    call join(group, group(i,j),group(i1,j), largest_label)
                    call join(group, group(i,j),group(i,j1), largest_label)
                end if
            end if
        end if
    end subroutine

    subroutine cluster(s, key)
        real(8),dimension(LENGTH,LENGTH,3) :: s
        integer,dimension(LENGTH,LENGTH) :: group, bond
        real(8),dimension(3) :: sx, sx_rigth, sx_down, w
        integer :: largest_label, k
        character(30) :: key
        w = random_vector()
        largest_label = 0
        bond(:,:) = 0
        group(:,:) = 0
        do j=1, LENGTH
            do i=1, LENGTH
                sx = s(i, j,:)
                sx_rigth = s(modl(i+1),j,:)
                sx_down = s(i,modl(j+1),:)
                if (is_bond(sx,sx_rigth,w)) then
                    bond(i,j) = 10
                end if
                if (is_bond(sx,sx_down,w)) then
                    bond(i,j) = bond(i,j)+1
                end if
                call hoshen_kopelman(group, bond, i, j, largest_label)
            end do
        end do

        do j=1, LENGTH
            do i=1, LENGTH
                call hoshen_kopelman(group, bond, i,j, largest_label)
            end do
        end do
        if (key=='single') then
            k = group(random_integer(LENGTH), random_integer(LENGTH))
            do i=1 , LENGTH
                do j=1, LENGTH
                    if (group(i,j)==k) then
                        s(i,j,:) = wolff_reflection(s(i,j,:),w)
                    end if
                end do
            end do
        else if (key=='multi') then
            do k=1, largest_label
                if (random()<=0.5) then
                    do j=1, LENGTH
                        do i=1, LENGTH
                            if (group(i,j)==k) then
                                s(i,j,:) = wolff_reflection(s(i,j,:),w)
                            end if
                        end do
                    end do
                end if
            end do
        end if 
    end subroutine

    subroutine metropolis(s, key)
        real(8),dimension(LENGTH,LENGTH,3) :: s
        real(8),dimension(3) :: sx, sx_rigth, sx_down, sx_left, sx_up, r
        real(8) :: h1, h2, delta, p
        integer :: i, j, i1 , j1
        character(30) :: key
        do i1=1, LENGTH
            do j1=1, LENGTH
                if (key=='random') then
                    i = random_integer(LENGTH)
                    j = random_integer(LENGTH)
                else if (key=='lexic') then
                    i = i1
                    j = j1
                end if
                sx = s(i, j,:)
                sx_rigth = s(modl(i+1),j,:)
                sx_down = s(i,modl(j+1),:)
                sx_left = s(modl(i-1),j,:)
                sx_up = s(i,modl(j-1),:)
                r = random_vector()
                h1 = -dot_product(sx, sx_rigth)-dot_product(sx, sx_down) &
                    -dot_product(sx,sx_left)-dot_product(sx,sx_up)
                h2 = -dot_product(r, sx_rigth)-dot_product(r, sx_down) &
                    -dot_product(r,sx_left)-dot_product(r,sx_up)
                delta = h2-h1
                if (delta<=0) then
                    p = 1
                else
                    if (temp<=0.) then
                        p = 0
                    else 
                        p = exp(-beta*delta)
                    end if
                end if
                if (random()<=p) then
                    s(i,j,:) = r
                end if
            end do
        end do
    end subroutine

    subroutine glauber(s, key)
        real(8),dimension(LENGTH,LENGTH,3) :: s
        real(8),dimension(3) :: sx, sx_rigth, sx_down, sx_left, sx_up, r
        real(8) :: h1, h2, delta, p
        integer :: i, j, i1 , j1
        character(30) :: key
        do i1=1, LENGTH
            do j1=1, LENGTH
                if (key=='random') then
                    i = random_integer(LENGTH)
                    j = random_integer(LENGTH)
                else if (key=='lexic') then
                    i = i1
                    j = j1
                end if
                sx = s(i, j,:)
                sx_rigth = s(modl(i+1),j,:)
                sx_down = s(i,modl(j+1),:)
                sx_left = s(modl(i-1),j,:)
                sx_up = s(i,modl(j-1),:)
                r = random_vector()
                h1 = -dot_product(sx, sx_rigth)-dot_product(sx, sx_down) &
                    -dot_product(sx,sx_left)-dot_product(sx,sx_up)
                h2 = -dot_product(r, sx_rigth)-dot_product(r, sx_down) &
                    -dot_product(r,sx_left)-dot_product(r,sx_up)
                delta = h2-h1
                if (temp<=0.) then
                    if (delta>0) then
                        p = 0
                    else
                        p = 1
                    end if
                else
                    p = exp(-beta*delta)
                    p = p/(1+p)
                end if
                if (random()<=p) then
                    s(i,j,:) = r
                end if
            end do
        end do
    end subroutine

    subroutine step(s, key, alg)
        real(8),dimension(LENGTH,LENGTH,3) :: s
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