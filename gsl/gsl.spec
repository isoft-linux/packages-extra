Summary: The GNU Scientific Library for numerical analysis
Name: gsl
Version: 1.16
Release: 17%{?dist}
URL: http://www.gnu.org/software/gsl/
# info part of this package is under GFDL license
# eigen/nonsymmv.c and eigen/schur.c
# contains rutiens which are part of LAPACK - under BSD style license
License: GPLv3 and GFDL and BSD

Source: ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Patch0: gsl-1.10-lib64.patch
Patch2: gsl-bug39055.patch
BuildRequires: pkgconfig

%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.

%package devel
Summary: Libraries and the header files for GSL development
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, automake

%description devel
The gsl-devel package contains the header files necessary for 
developing programs using the GSL (GNU Scientific Library).

%prep
%setup -q
%patch0 -p1 -b .lib64
%patch2 -p1 -b .bug39055
iconv -f windows-1252 -t utf-8 THANKS  > THANKS.aux
touch -r THANKS THANKS.aux
mv THANKS.aux THANKS

%build
%configure CFLAGS="$CFLAGS -fgnu89-inline"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT install='install -p'
# remove unpackaged files from the buildroot
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# remove static libraries
rm -r $RPM_BUILD_ROOT%{_libdir}/*.a


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_libdir}/*so.*
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_mandir}/man1/gsl-histogram.1*
%{_mandir}/man1/gsl-randist.1*

%files devel
%doc AUTHORS COPYING
%{_bindir}/gsl-config*
%{_datadir}/aclocal/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gsl.pc
%{_mandir}/man1/gsl-config.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
