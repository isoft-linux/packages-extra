Summary: GNUstep Project Center 
Name: ProjectCenter 
Version: 0.6.2
Release: 2
Source: ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
License: see COPYING
BuildRequires: clang
Requires: clang
%description
GNUstep Project Center

%package -n ProjectCenter.framework 
Summary: ProjectCenter framework runtime 

%description -n ProjectCenter.framework 
This package contains the runtime libraries and resources of ProjectCenter framework.

%package -n ProjectCenter.framework-devel 
Summary: Development headers of ProjectCenter framework. 
Requires: ProjectCenter.framework = %{version}-%{release}

%description -n ProjectCenter.framework-devel
Development headers of ProjectCenter framework.


%prep
%setup
%build
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%dir %{_libdir}/GNUstep/Applications/ProjectCenter.app
%{_libdir}/GNUstep/Applications/ProjectCenter.app/*
%{_bindir}/ProjectCenter

%files -n ProjectCenter.framework
%attr(-,root,root) 
%dir %{_libdir}/GNUstep/Frameworks/ProjectCenter.framework
%{_libdir}/GNUstep/Frameworks/ProjectCenter.framework/*
%{_libdir}/*.so*
%exclude %{_libdir}/GNUstep/Frameworks/ProjectCenter.framework/Headers

%files -n ProjectCenter.framework-devel
%attr(-,root,root) 
%{_libdir}/GNUstep/Frameworks/ProjectCenter.framework/Headers
%{_includedir}/ProjectCenter

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.6.2-2
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.
