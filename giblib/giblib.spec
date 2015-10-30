Summary: Simple library and a wrapper for imlib2
Name: giblib
Version: 1.2.4
Release: 24%{?dist}
License: MIT
# It looks like this project has been abandoned...
URL: http://linuxbrit.co.uk/giblib/
Source: http://linuxbrit.co.uk/downloads/giblib-%{version}.tar.gz
Patch0: giblib-1.2.4-multilib.patch
BuildRequires: imlib2-devel

%description
giblib is a utility library used by many of the applications from
linuxbrit.co.uk. It incorporates doubly linked lists, some string
functions, and a wrapper for imlib2. The wrapper does two things.
It gives you access to fontstyles, which can be loaded from files,
saved to files or defined dynamically through the API. It also,
and more importantly, wraps imlib2's context API.


%package devel
Summary: Static library and header files for giblib
Requires: %{name} = %{version}-%{release}
Requires: imlib2-devel, pkgconfig

%description devel
Install this package if you intend to develop using the giblib library.


%prep
%setup -q
%patch0 -p1


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_prefix}/doc/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING ChangeLog
%{_libdir}/*.so.*

%files devel
%{_bindir}/*-config
%{_includedir}/*
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.2.4-24
- Rebuild

