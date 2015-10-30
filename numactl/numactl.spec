Name:		numactl
Summary:	Library for tuning for Non Uniform Memory Access machines
Version:	2.0.10
Release:	3%{?dist}
# libnuma is LGPLv2 and GPLv2
# numactl binaries are GPLv2 only
License:	GPLv2
URL:		ftp://oss.sgi.com/www/projects/libnuma/download
Source0:	ftp://oss.sgi.com/www/projects/libnuma/download/numactl-%{version}.tar.gz
Buildroot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libtool automake autoconf

ExcludeArch: s390 s390x %{arm}

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy.

%package libs
Summary: libnuma libraries
# There is a tiny bit of GPLv2 code in libnuma.c
License: LGPLv2 and GPLv2

%description libs
numactl-libs provides libnuma, a library to do allocations with
NUMA policy in applications.

%package devel
Summary: Development package for building Applications that use numa
Requires: %{name}-libs = %{version}-%{release}
License: LGPLv2 and GPLv2

%description devel
Provides development headers for numa library calls

%prep
%setup -q -n %{name}-%{version}

%build
./autogen.sh
./configure --prefix=/usr --libdir=%{_libdir}
make clean
make CFLAGS="$RPM_OPT_FLAGS -I."

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%post libs -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/numactl
%{_bindir}/numademo
%{_bindir}/numastat
%{_bindir}/memhog
%{_bindir}/migspeed
%{_bindir}/migratepages

%files libs
%defattr(-,root,root,-)
%{_libdir}/libnuma.so.1.0.0
%{_libdir}/libnuma.so.1

%files devel
%defattr(-,root,root,-)
%{_libdir}/libnuma.so
%exclude %{_libdir}/libnuma.a
%exclude %{_libdir}/libnuma.la
%{_includedir}/numa.h
%{_includedir}/numaif.h
%{_includedir}/numacompat1.h
%{_mandir}/man3/*.3*

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 2.0.10-3
- Initial build

