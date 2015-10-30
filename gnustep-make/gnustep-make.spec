Summary: GNUstep makefile package 
Name: gnustep-make
Version: 2.6.7
Release: 2
Source: ftp://ftp.gnustep.org/pub/gnustep/core/gnustep-make-%{version}.tar.gz
Source1:gnustep-vars.sh
License: see COPYING
BuildRequires: clang
Requires: clang

BuildArch: noarch
%description
The makefile package is a simple, powerful and extensible way to write
makefiles for a GNUstep-based project.  It allows the user to write a
project without having to deal with the complex issues associated with
configuration, building, installation, and packaging.  It also allows
the user to easily create cross-compiled binaries.

%prep
%setup

%build
%configure CC=clang CXX=clang++ --enable-objc-nonfragile-abi --enable-native-objc-exceptions
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
sed -i -e 's/-shared-libgcc//g' $RPM_BUILD_ROOT/usr/share/GNUstep/Makefiles/common.make
install -D -m0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/gnustep-vars.sh
%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%doc COPYING README
%{_bindir}/debugapp
%{_bindir}/gnustep-config
%{_bindir}/gnustep-tests
%{_bindir}/openapp
%{_bindir}/opentool
%dir %{_sysconfdir}/GNUstep
%{_sysconfdir}/GNUstep/GNUstep.conf
%{_sysconfdir}/profile.d/gnustep-vars.sh
%dir %{_datadir}/GNUstep/Makefiles
%{_datadir}/GNUstep/Makefiles/*
%{_mandir}/man1/*
%{_mandir}/man7/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.6.7-2
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

