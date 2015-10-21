Summary: GNUstep GUI Backend
Name: gnustep-back
Version: 0.24.1
Release: 1
Source: ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Group:  System Environment/Libraries 
License: see COPYING
BuildRequires: clang 
BuildRequires: libobjc2-devel
BuildRequires: gnustep-make
BuildRequires: gnustep-base-devel
BuildRequires: gnustep-gui-devel

%description
GNUstep GUI Backend
%prep
%setup

%build
%configure CC=clang CXX=clang++ 
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%doc COPYING README
%dir %{_libdir}/GNUstep/Fonts/Helvetica.nfont
%{_libdir}/GNUstep/Fonts/Helvetica.nfont/*
%dir %{_libdir}/GNUstep/Bundles/libgnustep-back-024.bundle
%{_libdir}/GNUstep/Bundles/libgnustep-back-024.bundle/*
%{_bindir}/gpbs
%{_mandir}/man1/gpbs.1.gz

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

