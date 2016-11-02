Name: libhddtemp
Version: 1.0.0
Release: 1
Summary: Get the temperature of harddisks.

License: GPLv2 or GPLv3
URL: git@git.isoft.zhcn.cc:zhaohongbo/libhddtemp.git
Source0: %{name}-%{version}.tar.gz

BuildRequires: glibc-headers
BuildRequires: glibc-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: intltool

%description
Get the temperature of harddisks.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
./autogen.sh
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_includedir}/libhddtemp

%changelog
* Tue Nov 01 2016 x - 0.1.0-2
- Version 0.1.0-1.

