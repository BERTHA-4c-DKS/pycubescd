program rotate
implicit none

real :: a(3), b(3), c(3), risu(3)
real :: phi, theta
real :: matx(3,3),maty(3,3),rotmat(3,3)
real,allocatable :: coordinates(:,:)
real,allocatable :: rotcoords(:,:)
character(len=3),allocatable :: names(:)
CHARACTER (LEN=128) :: infile1, outfile, msg

integer :: ierr,i,j,natoms

! This program rotate a vector along the z axis 
! The program assumes the order x, y, z in the input file
! The program assumes that the the rotation matrix is determined
! by the rotation of the vector position coordinates(3,1) --> (0,0,z1) 
! Assume the zero coordinates(3,2) --> (0,0,z1) 
! 

WRITE(UNIT=*,FMT=*) "Set the center 1 and 2 along the z axis. Center 2 is fixed as origin"
WRITE (UNIT=msg, FMT=*) "Usage: rotate_z <infile1>  <outfile>"

CALL getarg (1, infile1)
CALL error_check_arg ( infile1, msg)
CALL getarg (2, outfile)
CALL error_check_arg ( outfile, msg)


open(UNIT=17,file=infile1,STATUS='OLD',ACTION='READ')
read(17,FMT='(I4)') natoms
read(17,*) 
!
ALLOCATE(coordinates(3,natoms), STAT=ierr)
ALLOCATE(names(natoms), STAT=ierr)
!
do i=1,natoms
read(17,*) names(i),(coordinates(j,i),j=1,3)
enddo
close(17)

!Translation atoms(2) to zero

a(:) = coordinates(:,2)
 
do i=1,natoms
coordinates(:,i) = coordinates(:,i)- a(:)
enddo

print*, coordinates(:,1)

print*, coordinates(:,2)


!
!do i=1,natoms
!write(*,FMT='(A3,2X,3(F10.7,2X))') names(i),(coordinates(j,i),j=1,3)
!enddo

! The program assumes that the the rotation matrix is determined
! by the rotation of the vector position coordinates(3,1) --> (0,0,z1) 
a(:)=coordinates(:,1)

! Rotation along x 

phi = atan(a(2)/a(3))

print *,"Phi =", phi


matx(1,1) = 1.0d0
matx(1,2) = 0.0d0
matx(1,3) = 0.0d0
matx(2,1) = 0.0d0
matx(2,2) = cos(phi) 
matx(2,3) = -sin(phi)
matx(3,1) = 0.0d0
matx(3,2) = sin(phi) 
matx(3,3) = cos(phi)

!print *, matx(:,:)

do i=1,3
 b(i) = DOT_PRODUCT(matx(i,:),a(:)) 
enddo

theta = atan(-b(1)/b(3))

maty(1,1) = cos(theta)
maty(1,2) = 0.0d0
maty(1,3) = sin(theta)
maty(2,1) = 0.0d0
maty(2,2) = 1.0d0
maty(2,3) = 0.0d0
maty(3,1) = -sin(theta)
maty(3,2) = 0.0d0 
maty(3,3) = cos(theta)


rotmat = MATMUL(maty,matx)

ALLOCATE(rotcoords(3,natoms),STAT=ierr)

 rotcoords = MATMUL(rotmat,coordinates)

open(UNIT=18,file=outfile,STATUS='UNKNOWN',ACTION='WRITE')
!
!
write(18,FMT='(I4)') natoms 
write(18,*) 
do i=1,natoms
write(18,FMT='(A4,2X,3(F10.4,2X))') names(i),(rotcoords(j,i),j=1,3)
enddo


DEALLOCATE(names,rotcoords,coordinates)
close(18)

end program

SUBROUTINE error_check_arg ( arg, msg )
    ! in
CHARACTER (LEN=*), INTENT(IN) :: arg, msg

IF ( arg == "") THEN
      PRINT *, msg
      STOP
ENDIF

END SUBROUTINE error_check_arg
