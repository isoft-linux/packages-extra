%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Patch version?
%global snaprel -patch1

# NOTE:  Try not to release new versions to released versions of Fedora
# You need to recompile all users of HDF5 for each version change
Name: hdf5
Version: 1.8.15
Release: 4.patch1%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD
Group: System Environment/Libraries
URL: http://www.hdfgroup.org/HDF5/

Source0: http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-%{version}%{?snaprel}/src/hdf5-%{version}%{?snaprel}.tar.bz2
Source1: h5comp
# For man pages
Source2: http://ftp.us.debian.org/debian/pool/main/h/hdf5/hdf5_1.8.14+docs-3.debian.tar.xz
Patch0: hdf5-LD_LIBRARY_PATH.patch
# Fix -Werror=format-security errors
Patch2: hdf5-format.patch
# Fix long double conversions on ppc64le
# https://bugzilla.redhat.com/show_bug.cgi?id=1078173
Patch3: hdf5-ldouble-ppc64le.patch

BuildRequires: krb5-devel, openssl-devel, zlib-devel, gcc-gfortran, time
# For patches/rpath
BuildRequires: automake
BuildRequires: libtool

%global with_mpich 0 
%global with_openmpi 0

%if %{with_mpich}
%global mpi_list mpich
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF5 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF5 files according to your needs.


%package devel
Summary: HDF5 development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel

%description devel
HDF5 development headers and libraries.


%package static
Summary: HDF5 static libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
HDF5 static libraries.


%if %{with_mpich}
%package mpich
Summary: HDF5 mpich libraries
Group: Development/Libraries
Requires: mpich
BuildRequires: mpich-devel
Provides: %{name}-mpich2 = %{version}-%{release}
Obsoletes: %{name}-mpich2 < 1.8.11-4

%description mpich
HDF5 parallel mpich libraries


%package mpich-devel
Summary: HDF5 mpich development files
Group: Development/Libraries
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: mpich
Provides: %{name}-mpich2-devel = %{version}-%{release}
Obsoletes: %{name}-mpich2-devel < 1.8.11-4

%description mpich-devel
HDF5 parallel mpich development files


%package mpich-static
Summary: HDF5 mpich static libraries
Group: Development/Libraries
Requires: %{name}-mpich-devel%{?_isa} = %{version}-%{release}
Provides: %{name}-mpich2-static = %{version}-%{release}
Obsoletes: %{name}-mpich2-static < 1.8.11-4

%description mpich-static
HDF5 parallel mpich static libraries
%endif


%if %{with_openmpi}
%package openmpi
Summary: HDF5 openmpi libraries
Group: Development/Libraries
Requires: openmpi
BuildRequires: openmpi-devel

%description openmpi
HDF5 parallel openmpi libraries


%package openmpi-devel
Summary: HDF5 openmpi development files
Group: Development/Libraries
Requires: %{name}-openmpi%{_isa} = %{version}-%{release}
Requires: openmpi-devel

%description openmpi-devel
HDF5 parallel openmpi development files


%package openmpi-static
Summary: HDF5 openmpi static libraries
Group: Development/Libraries
Requires: %{name}-openmpi-devel%{?_isa} = %{version}-%{release}

%description openmpi-static
HDF5 parallel openmpi static libraries
%endif


%prep
%setup -q -a 2 -n %{name}-%{version}%{?snaprel}
%patch0 -p1 -b .LD_LIBRARY_PATH
%patch2 -p1 -b .format
%patch3 -p1 -b .ldouble-ppc64le
#This should be fixed in 1.8.7
find \( -name '*.[ch]*' -o -name '*.f90' -o -name '*.txt' \) -exec chmod -x {} +
autoreconf -f -i


%build
#Do out of tree builds
%global _configure ../configure
#Common configure options
%global configure_opts \\\
  --disable-silent-rules \\\
  --enable-fortran \\\
  --enable-fortran2003 \\\
  --enable-hl \\\
  --enable-shared \\\
%{nil}
# --enable-cxx and --enable-parallel flags are incompatible
# --with-mpe=DIR          Use MPE instrumentation [default=no]
# --enable-cxx/fortran/parallel and --enable-threadsafe flags are incompatible

#Serial build
export CC=gcc
export CXX=g++
export F9X=gfortran
mkdir build
pushd build
ln -s ../configure .
%configure \
  %{configure_opts} \
  --enable-cxx
make
popd

#MPI builds
export CC=mpicc
export CXX=mpicxx
export F9X=mpif90
for mpi in %{?mpi_list}
do
  mkdir $mpi
  pushd $mpi
  module load mpi/$mpi-%{_arch}
  ln -s ../configure .
  %configure \
    %{configure_opts} \
    --enable-parallel \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share \
    --mandir=%{_libdir}/$mpi/share/man
  make
  module purge
  popd
done


%install
make -C build install DESTDIR=${RPM_BUILD_ROOT}
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
for mpi in %{?mpi_list}
do
  module load mpi/$mpi-%{_arch}
  make -C $mpi install DESTDIR=${RPM_BUILD_ROOT}
  rm $RPM_BUILD_ROOT/%{_libdir}/$mpi/lib/*.la
  module purge
done
#Fortran modules
mkdir -p ${RPM_BUILD_ROOT}%{_fmoddir}
mv ${RPM_BUILD_ROOT}%{_includedir}/*.mod ${RPM_BUILD_ROOT}%{_fmoddir}
#Fixup example permissions
find ${RPM_BUILD_ROOT}%{_datadir} \( -name '*.[ch]*' -o -name '*.f90' \) -exec chmod -x {} +

#Fixup headers and scripts for multiarch
%ifarch x86_64 ppc64 ia64 s390x sparc64 alpha
sed -i -e s/H5pubconf.h/H5pubconf-64.h/ ${RPM_BUILD_ROOT}%{_includedir}/H5public.h
mv ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf.h \
   ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf-64.h
for x in h5c++ h5cc h5fc
do
  mv ${RPM_BUILD_ROOT}%{_bindir}/${x} \
     ${RPM_BUILD_ROOT}%{_bindir}/${x}-64
  install -m 0755 %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/${x}
done
%else
sed -i -e s/H5pubconf.h/H5pubconf-32.h/ ${RPM_BUILD_ROOT}%{_includedir}/H5public.h
mv ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf.h \
   ${RPM_BUILD_ROOT}%{_includedir}/H5pubconf-32.h
for x in h5c++ h5cc h5fc
do
  mv ${RPM_BUILD_ROOT}%{_bindir}/${x} \
     ${RPM_BUILD_ROOT}%{_bindir}/${x}-32
  install -m 0755 %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/${x}
done
%endif
# rpm macro for version checking
mkdir -p ${RPM_BUILD_ROOT}%{macrosdir}
cat > ${RPM_BUILD_ROOT}%{macrosdir}/macros.hdf5 <<EOF
# HDF5 version is
%%_hdf5_version	%{version}
EOF

# Install man pages from debian
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
cp -p debian/man/*.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/
for mpi in %{?mpi_list}
do
  mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/$mpi/share/man/man1
  cp -p debian/man/h5p[cf]c.1 ${RPM_BUILD_ROOT}%{_libdir}/$mpi/share/man/man1/
done
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/h5p[cf]c.1


%check
make -C build check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{_bindir}/gif2h5
%{_bindir}/h52gif
%{_bindir}/h5copy
%{_bindir}/h5debug
%{_bindir}/h5diff
%{_bindir}/h5dump
%{_bindir}/h5import
%{_bindir}/h5jam
%{_bindir}/h5ls
%{_bindir}/h5mkgrp
%{_bindir}/h5perf_serial
%{_bindir}/h5repack
%{_bindir}/h5repart
%{_bindir}/h5stat
%{_bindir}/h5unjam
%{_libdir}/*.so.10*
%{_mandir}/man1/gif2h5.1*
%{_mandir}/man1/h52gif.1*
%{_mandir}/man1/h5copy.1*
%{_mandir}/man1/h5diff.1*
%{_mandir}/man1/h5dump.1*
%{_mandir}/man1/h5import.1*
%{_mandir}/man1/h5jam.1*
%{_mandir}/man1/h5ls.1*
%{_mandir}/man1/h5mkgrp.1*
%{_mandir}/man1/h5perf_serial.1*
%{_mandir}/man1/h5repack.1*
%{_mandir}/man1/h5repart.1*
%{_mandir}/man1/h5stat.1*
%{_mandir}/man1/h5unjam.1*

%files devel
%{macrosdir}/macros.hdf5
%{_bindir}/h5c++*
%{_bindir}/h5cc*
%{_bindir}/h5fc*
%{_bindir}/h5redeploy
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.settings
%{_fmoddir}/*.mod
%{_datadir}/hdf5_examples/
%{_mandir}/man1/h5c++.1*
%{_mandir}/man1/h5cc.1*
%{_mandir}/man1/h5debug.1*
%{_mandir}/man1/h5fc.1*
%{_mandir}/man1/h5redeploy.1*

%files static
%{_libdir}/*.a

%if %{with_mpich}
%files mpich
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{_libdir}/mpich/bin/gif2h5
%{_libdir}/mpich/bin/h52gif
%{_libdir}/mpich/bin/h5copy
%{_libdir}/mpich/bin/h5debug
%{_libdir}/mpich/bin/h5diff
%{_libdir}/mpich/bin/h5dump
%{_libdir}/mpich/bin/h5import
%{_libdir}/mpich/bin/h5jam
%{_libdir}/mpich/bin/h5ls
%{_libdir}/mpich/bin/h5mkgrp
%{_libdir}/mpich/bin/h5redeploy
%{_libdir}/mpich/bin/h5repack
%{_libdir}/mpich/bin/h5perf
%{_libdir}/mpich/bin/h5perf_serial
%{_libdir}/mpich/bin/h5repart
%{_libdir}/mpich/bin/h5stat
%{_libdir}/mpich/bin/h5unjam
%{_libdir}/mpich/bin/ph5diff
%{_libdir}/mpich/lib/*.so.10*

%files mpich-devel
%{_includedir}/mpich-%{_arch}
%{_libdir}/mpich/bin/h5pcc
%{_libdir}/mpich/bin/h5pfc
%{_libdir}/mpich/lib/lib*.so
%{_libdir}/mpich/lib/lib*.settings
%{_libdir}/mpich/share/man/man1/h5pcc.1*
%{_libdir}/mpich/share/man/man1/h5pfc.1*

%files mpich-static
%{_libdir}/mpich/lib/*.a
%endif

%if %{with_openmpi}
%files openmpi
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{_libdir}/openmpi/bin/gif2h5
%{_libdir}/openmpi/bin/h52gif
%{_libdir}/openmpi/bin/h5copy
%{_libdir}/openmpi/bin/h5debug
%{_libdir}/openmpi/bin/h5diff
%{_libdir}/openmpi/bin/h5dump
%{_libdir}/openmpi/bin/h5import
%{_libdir}/openmpi/bin/h5jam
%{_libdir}/openmpi/bin/h5ls
%{_libdir}/openmpi/bin/h5mkgrp
%{_libdir}/openmpi/bin/h5perf
%{_libdir}/openmpi/bin/h5perf_serial
%{_libdir}/openmpi/bin/h5redeploy
%{_libdir}/openmpi/bin/h5repack
%{_libdir}/openmpi/bin/h5repart
%{_libdir}/openmpi/bin/h5stat
%{_libdir}/openmpi/bin/h5unjam
%{_libdir}/openmpi/bin/ph5diff
%{_libdir}/openmpi/lib/*.so.10*

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}
%{_libdir}/openmpi/bin/h5pcc
%{_libdir}/openmpi/bin/h5pfc
%{_libdir}/openmpi/lib/lib*.so
%{_libdir}/openmpi/lib/lib*.settings
%{_libdir}/openmpi/share/man/man1/h5pcc.1*
%{_libdir}/openmpi/share/man/man1/h5pfc.1*

%files openmpi-static
%{_libdir}/openmpi/lib/*.a
%endif


%changelog
