Name:           libspnav
Version:        0.2.3
Release:        4%{?dist}
Summary:        Open source alternative to 3DConnextion drivers

License:        BSD
URL:            http://spacenav.sourceforge.net/
Source:         http://downloads.sourceforge.net/spacenav/%{name}-%{version}.tar.gz

Patch0:         libspnav-0.2.3-lib_links.patch

BuildRequires:  libX11-devel


%description
The spacenav project provides a free, compatible alternative to the proprietary
3Dconnexion device driver and SDK, for their 3D input devices (called "space
navigator", "space pilot", "space traveller", etc).

This package provides the library needed for applications to connect to the 
user land daemon.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.


%prep
%setup -q
%patch0 -p1 -b .lib_links


%build
# Set libdir properly
sed -i "s/libdir=lib/libdir=%{_lib}/g" configure
%configure 
sed -i "s/CFLAGS =/CFLAGS +=/g" Makefile
make %{?_smp_mflags}


%install
%make_install

# Remove static library
rm -f %{buildroot}%{_libdir}/%{name}.a


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/*.so.0*

%files devel
%doc examples
%{_libdir}/*.so
%{_includedir}/*.h


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2.3-4
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.2.3-3
- Initial build

