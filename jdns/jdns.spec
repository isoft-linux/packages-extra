Name:           jdns
Version:        2.0.3
Release:        2%{?dist}
Summary:        A simple DNS queries library

License:        MIT
URL:            http://delta.affinix.com/jdns/
Source0:        http://delta.affinix.com/download/%{name}-%{version}.tar.bz2

## upstream patches

## upstreamable patches

BuildRequires:  cmake
BuildRequires:  pkgconfig(QtCore) pkgconfig(QtNetwork)
BuildRequires:  pkgconfig(Qt5Core) pkgconfig(Qt5Network)

%description
JDNS is a simple DNS implementation that can perform normal DNS
queries of any record type (notably SRV), as well as Multicast DNS
queries and advertising. Multicast support is based on Jeremie
Miller's "mdnsd" implementation.

For maximum flexibility, JDNS is written in C with no direct
dependencies, and is licensed under the MIT license. Your application
must supply functionality to JDNS, such as UDP sending/receiving, via
callbacks.

Qt-based command-line tool called ‘jdns’ that can be used to test
functionality.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     qjdns-qt4
Summary:        Qt4-wrapper for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      qjdns < %{version}-%{release}
Provides:       qjdns = %{version}-%{release}

# avoid abi breaking
%if 0%{?__isa_bits} == 64
Provides:       libqjdns.so.2()(64bit)
%else
Provides:       libqjdns.so.2
%endif

%description -n qjdns-qt4
For Qt4 users there is a wrapper available called QJDns and a very
high-level wrapper called QJDnsShared (under its original name
JDnsShared).

Qt-based command-line tool called ‘jdns’ that can be used to test
functionality.

%package -n     qjdns-qt4-devel
Summary:        Development files for qjdns-qt4
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes:      qjdns-devel < %{version}-%{release}
Provides:       qjdns-devel = %{version}-%{release}
Requires:       qjdns-qt4%{?_isa} = %{version}-%{release}
%description -n qjdns-qt4-devel
The qjdns-qt4-devel package contains libraries and header files for
developing applications that use qjdns-qt4.

%package -n     qjdns-qt5
Summary:        Qt5-wrapper for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description -n qjdns-qt5
For Qt5 users there is a wrapper available called QJDns and a very
high-level wrapper called QJDnsShared (under its original name
JDnsShared).

%package -n     qjdns-qt5-devel
Summary:        Development files for qjdns-qt5
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       qjdns-qt5%{?_isa} = %{version}-%{release}
%description -n qjdns-qt5-devel
The qjdns-qt5-devel package contains libraries and header files for
developing applications that use qjdns-qt5.


%prep
%setup -q


%build
mkdir %{_target_platform}-qt5
pushd %{_target_platform}-qt5
# FIXME: JDNS_TOOL FTBFS due to -fPIC/-fPIE wierdness, omit for now -- rex
%{cmake} .. \
  -DBUILD_JDNS_TOOL:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING="Release"

make %{?_smp_mflags}
popd

mkdir %{_target_platform}-qt4
pushd %{_target_platform}-qt4
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DQT4_BUILD:BOOL=ON

make %{?_smp_mflags}
popd


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt4

# Avoid api/abi breaking wich introduced with jdns-2.0.3
ln -s libqjdns-qt4.so.2 %{buildroot}%{_libdir}/libqjdns.so.2
ln -s qjdns-qt4.pc %{buildroot}%{_libdir}/pkgconfig/qjdns.pc

%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
# The pkg-config versions should match the tarball version
test "$(pkg-config --modversion jdns)" = "%{version}"
test "$(pkg-config --modversion qjdns)" = "%{version}"
test "$(pkg-config --modversion qjdns-qt4)" = "%{version}"
test "$(pkg-config --modversion qjdns-qt5)" = "%{version}"


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README.md
%{_libdir}/libjdns.so.2*

%files devel
%dir %{_includedir}/jdns/
%{_includedir}/jdns/jdns.h
%{_includedir}/jdns/jdns_export.h
%{_libdir}/libjdns.so
%{_libdir}/cmake/jdns/
%{_libdir}/pkgconfig/jdns.pc

%post -n qjdns-qt4 -p /sbin/ldconfig
%postun -n qjdns-qt4 -p /sbin/ldconfig

%files -n qjdns-qt4
%{_bindir}/jdns
%{_libdir}/libqjdns.so.2
%{_libdir}/libqjdns-qt4.so.2*

%files -n qjdns-qt4-devel
%{_includedir}/jdns/qjdns.h
%{_includedir}/jdns/qjdnsshared.h
%{_libdir}/libqjdns-qt4.so
%{_libdir}/cmake/qjdns/
%{_libdir}/cmake/qjdns-qt4/
%{_libdir}/pkgconfig/qjdns.pc
%{_libdir}/pkgconfig/qjdns-qt4.pc

%post -n qjdns-qt5 -p /sbin/ldconfig
%postun -n qjdns-qt5 -p /sbin/ldconfig

%files -n qjdns-qt5
%{_libdir}/libqjdns-qt5.so.2*

%files -n qjdns-qt5-devel
%{_includedir}/jdns/qjdns.h
%{_includedir}/jdns/qjdnsshared.h
%{_libdir}/libqjdns-qt5.so
%{_libdir}/cmake/qjdns/
%{_libdir}/cmake/qjdns-qt5/
%{_libdir}/pkgconfig/qjdns-qt5.pc


%changelog
* Wed Dec 02 2015 sulit <sulitsrc@gmail.com> - 2.0.3-2
- Init for isoft4
- Don't disable qt4 and it can be required others
- qt5 ABI change
