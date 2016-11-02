Name: ph_sensor
Version: 1.0.0
Release: 1
Summary: This lib is used to get sensors tem.

License: GPLv2 or GPLv3
URL: git@git.isoft.zhcn.cc:zhaohongbo/ph_sensor.git
Source0: %{name}-%{version}.tar.gz

BuildRequires: libgtop2-devel
BuildRequires: lm_sensors-libs
BuildRequires: lm_sensors-devel
BuildRequires: libatasmart-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: intltool

Requires: libgtop2
Requires: lm_sensors
Requires: libatasmart

%description
This lib is used to get sensors tem.

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
%{_includedir}/libphsensor

%changelog
* Tue Nov 01 2016 x - 0.1.0-2
- Version 0.1.0-1.

