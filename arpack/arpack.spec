Name:		arpack
Version:	3.1.5
Release:	2%{?dist}
Summary:	Fortran 77 subroutines for solving large scale eigenvalue problems
License:	BSD
Group:		Development/Libraries
URL:		http://forge.scilab.org/index.php/p/arpack-ng/
Source0:	http://forge.scilab.org/index.php/p/arpack-ng/downloads/get/arpack-ng_%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc-gfortran
BuildRequires:	atlas-devel
Provides:	arpack-ng = %{version}-%{release}

%description
ARPACK is a collection of Fortran 77 subroutines designed to solve large 
scale eigenvalue problems. 

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

%package devel
Summary:	Files needed for developing arpack based applications
Group:		Development/Libraries
Requires:	arpack = %{version}-%{release}
Provides:	arpack-ng-devel = %{version}-%{release}

%description devel
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the so
library links used for building arpack based applications.

%package doc
Summary:	Examples for the use of arpack
Group:		Documentation
BuildArch: noarch

%description doc
This package contains examples for the use of arpack.

%package static
Summary:	Static library for developing arpack based applications
Group:		Development/Libraries
Requires:	arpack-devel = %{version}-%{release}
Provides:	arpack-ng-static = %{version}-%{release}

%description static
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the static
library and so links used for building arpack based applications.

%prep
%setup -q -n arpack-ng-%{version} 

%build
export F77=gfortran
%global atlaslib -L%{_libdir}/atlas -ltatlas
%configure --enable-shared --enable-static \
    --with-blas="%{atlaslib}" \
    --with-lapack="%{atlaslib}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Get rid of .la files
rm -r %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check
pushd EXAMPLES ; make clean ; popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING
%{_libdir}/libarpack.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/arpack.pc
%{_libdir}/libarpack.so

%files doc
%defattr(-,root,root,-)
%doc EXAMPLES/ DOCUMENTS/

%files static
%defattr(-,root,root,-)
%{_libdir}/libarpack.a

%changelog
