Summary: GNUstep Renaissance is a development framework that reads XML descriptions of GUI. 
Name: gnustep-Renaissance
Version: 0.9.0 
Release: 1
URL:    http://www.gnustep.it/Renaissance/index.html
Source0: http://www.gnustep.it/Renaissance/Download/Renaissance-%{version}.tar.gz
Group:  Development/Tools
License: LGPL
BuildRequires: clang gnustep-make libobjc2-devel
Requires: %{name}-lib = %{version}-%{release}
%description
GNUstep Renaissance is free software (GNU LGPL), and part of the GNUstep project. It is a development framework which runs on top of the GNUstep libraries or on top of the Apple Mac OS X Cocoa frameworks, providing an opaque layer to write portable applications. 

%package lib 
Summary: Runtime library of Renaissance
Group: System Environment/Libraries 

%description lib
this package contains runtime library of Renaissance. 

%package lib-devel
Summary: Development headers and libraries of Renaissance 
Group: Development/Libraries
Requires: %{name}-lib = %{version}-%{release}

%description lib-devel
this package contains header files and libraries necessary
for developing programs using Renaissance. 

%prep
%setup -n Renaissance-%{version}
%build
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%{_bindir}/GSMarkupBrowser
%{_bindir}/GSMarkupLocalizableStrings
%dir %{_libdir}/GNUstep/Applications/GSMarkupBrowser.app
%{_libdir}/GNUstep/Applications/GSMarkupBrowser.app/*
%dir %{_libdir}/GNUstep/Applications/GSMarkupLocalizableStrings.app
%{_libdir}/GNUstep/Applications/GSMarkupLocalizableStrings.app/*

%files lib 
%attr(-,root,root)
%{_libdir}/libRenaissance.so.*

%files lib-devel
%attr(-,root,root)
%dir %{_includedir}/Renaissance
%{_includedir}/Renaissance/*
%{_libdir}/libRenaissance.so
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

