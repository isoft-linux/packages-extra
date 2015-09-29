Name:		qrupdate
Version:	1.1.2
Release:	7%{?dist}
Summary:	A Fortran library for fast updates of QR and Cholesky decompositions
Group:		Development/Libraries
License:	GPLv3+
URL:		http://qrupdate.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc-gfortran

# These are needed for the test phase
BuildRequires:	blas-devel
BuildRequires:	lapack-devel

%description
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions. 

%package devel
Summary:	Development libraries for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development libraries for %{name}.

%prep
%setup -q
# Modify install location
sed -i 's|$(PREFIX)/lib/|$(DESTDIR)%{_libdir}/|g' src/Makefile

%build
make solib FC=gfortran FFLAGS="%{optflags} -fimplicit-none -funroll-loops" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install-shlib LIBDIR=%{_libdir} PREFIX="%{buildroot}"
# Verify attributes
chmod 755 %{buildroot}%{_libdir}/libqrupdate.*

%clean
rm -rf %{buildroot}

%check
make test FC=gfortran FFLAGS="%{optflags} -fimplicit-none -funroll-loops"

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_libdir}/libqrupdate.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libqrupdate.so


%changelog
