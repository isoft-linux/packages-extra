Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.10.0
Release: 2
License: MIT
URL: http://c-ares.haxx.se/
Source0: http://c-ares.haxx.se/download/%{name}-%{version}.tar.gz
Patch0: 0001-Use-RPM-compiler-options.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

%description
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named 'ares', written 
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%prep
%setup -q
%patch0 -p1 -b .optflags

%build
autoreconf -if
%configure --enable-shared --disable-static \
           --disable-dependency-tracking
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-2
- Rebuild

