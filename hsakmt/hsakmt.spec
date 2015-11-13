Name: hsakmt
Version: 1.0.0
Release: 2
Summary: A thunk library to provide a user-space interface to the AMD HSA Linux kernel driver
License: see COPYING 
URL: http://xorg.freedesktop.org 
Source0: http://xorg.freedesktop.org/releases/individual/lib/hsakmt-1.0.0.tar.bz2

BuildRequires: pkgconfig	

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%license COPYING
%{_libdir}/libhsakmt-1.so.*

%files devel
%dir %{_includedir}/hsakmt-1
%{_includedir}/hsakmt-1/*
%{_libdir}/libhsakmt-1.a
%{_libdir}/libhsakmt-1.so
%{_libdir}/pkgconfig/hsakmt-1.pc

%changelog
* Wed Nov 11 2015 Cjacker <cjacker@foxmail.com>
- Initial build


