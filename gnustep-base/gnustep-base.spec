Summary: GNUstep Base Library 
Name: gnustep-base
Version: 1.24.8
Release: 3
Source: ftp://ftp.gnustep.org/pub/gnustep/core/gnustep-base-%{version}.tar.gz
Patch0: gnustep-fix-objc++.patch
License: see COPYING
BuildRequires: clang gnustep-make libobjc2-devel
BuildRequires: libxml2-devel libxslt-devel libffi-devel
BuildRequires: libicu-devel avahi-devel gnutls-devel gmp-devel
BuildRequires: gnutls-devel
BuildRequires: libdispatch
BuildRequires: zlib-devel
 
Requires: libobjc2


%description
The GNUstep Base Library is a library of general-purpose, non-graphical
Objective C objects.  For example, it includes classes for strings,
object collections, byte streams, typed coders, invocations,
notifications, notification dispatchers, moments in time, network ports,
remote object messaging support (distributed objects), and event loops.

It provides functionality that aims to implement the non-graphical
portion of the Apple's Cocoa frameworks (the Foundation library) which
came from the OpenStep standard.


%package devel
Summary: Development tools for gnustep-base 
Requires: %{name} = %{version}-%{release}

%description devel
The gnustep-base-devel package contains header files and documentation necessary
for developing programs using gnustep.

%prep
%setup
%patch0 -p1

%build
%configure CC=clang CXX=clang++ --disable-mixedabi
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#we own these folders
mkdir -p $RPM_BUILD_ROOT%{_libdir}/GNUstep/Applications
mkdir -p $RPM_BUILD_ROOT%{_libdir}/GNUstep/Frameworks
mkdir -p $RPM_BUILD_ROOT%{_libdir}/GNUstep/Bundles

%check
make check ||:

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%doc COPYING README
%{_bindir}/*
%dir %{_datadir}/GNUstep/Makefiles/Additional
%{_datadir}/GNUstep/Makefiles/Additional/base.make
%dir %{_libdir}/GNUstep
%dir %{_libdir}/GNUstep/DTDs
%dir %{_libdir}/GNUstep/Libraries
%ghost %{_libdir}/GNUstep/Applications
%ghost %{_libdir}/GNUstep/Frameworks
%ghost %{_libdir}/GNUstep/Bundles
%{_libdir}/GNUstep/DTDs/*
%dir %{_libdir}/GNUstep/Libraries/gnustep-base
%{_libdir}/GNUstep/Libraries/gnustep-base/*
%{_libdir}/libgnustep-base.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%attr(-,root,root)
%{_includedir}/* 
%{_libdir}/*.so
%changelog
* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 1.24.8-3
- Rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.24.8-2
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

