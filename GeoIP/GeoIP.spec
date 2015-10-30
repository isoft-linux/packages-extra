# Tests require network access so fail in koji; build using --with tests to run them yourself
%bcond_with tests

Name:		GeoIP
Version:	1.6.5
Release:	4%{?dist}
Summary:	Library for country/city/organization to IP address or hostname mapping
License:	LGPLv2+
URL:		http://www.maxmind.com/app/c
Source0:	https://github.com/maxmind/geoip-api-c/releases/download/v%{version}/GeoIP-%{version}.tar.gz
BuildRequires:	zlib-devel

Requires:	GeoIP-GeoLite-data

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from.

It uses file based databases that can optionally be updated on a weekly basis
by installing the geoipupdate-cron (IPv4) and/or geoipupdate-cron6 (IPv6)
packages.

%package devel
Summary:	Development headers and libraries for GeoIP
Requires:	%{name} = %{version}-%{release}
Provides:	geoip-devel = %{version}-%{release}
Obsoletes:	geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications.

%prep
%setup -q

%build
%configure --disable-static --disable-dependency-tracking

# Kill bogus rpaths
sed -i -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install

# nix the stuff we don't need like .la files.
rm -f %{buildroot}%{_libdir}/*.la

%check
# Tests require network access so fail in koji; build using --with tests to run them yourself
%{?with_tests:LD_LIBRARY_PATH=%{buildroot}%{_libdir} make check}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%doc AUTHORS ChangeLog NEWS.md README.md
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%{_libdir}/libGeoIP.so.1
%{_libdir}/libGeoIP.so.1.*
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*

%files devel
%{_includedir}/GeoIP.h
%{_includedir}/GeoIPCity.h
%{_libdir}/libGeoIP.so
%{_libdir}/pkgconfig/geoip.pc

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.6.5-4
- Rebuild

