Summary: SPICE protocol headers 
Name: spice-protocol
Version: 0.12.7
Release: 1
License: LGPLv2+
Group: System Environment/Libraries
Url:    http://www.spice-space.org
Source: %{name}-%{version}.tar.bz2

%description
SPICE protocol headers

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root, -)
%dir %{_includedir}/spice-1
%{_includedir}/spice-1/*
%{_datadir}/pkgconfig/spice-protocol.pc

