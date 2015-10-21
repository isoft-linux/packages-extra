Summary: Graphical interface builder
Name:    Gorm
Version: 1.2.18
Release: 1
Source:  ftp://ftp.gnustep.org/pub/gnustep/core/gorm-%{version}.tar.gz
License: see COPYING
BuildRequires: clang
Requires: clang
%description
Graphical interface builder

%prep
%setup -n gorm-%{version}

%build
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
/
