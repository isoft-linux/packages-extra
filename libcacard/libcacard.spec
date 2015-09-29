#it's part of qemu, since spice need libcacard and qemu need spice library.
#here seperate it.

%define _udevdir %{_libdir}/udev/rules.d

Summary: Common Access Card (CAC) Emulation Development library
Name:    libcacard 
Version: 2.4.0
Release: 1
License: GPLv2+ and LGPLv2+ and BSD
URL: http://www.qemu.org/
Source0: qemu-%{version}.tar.bz2

BuildRequires: zlib-devel which
BuildRequires: ncurses-devel
BuildRequires: nss-devel nspr-devel glib2-devel

%description
Common Access Card (CAC) Emulation

%package devel
Summary:   CAC Emulation devel
Requires:  libcacard = %{version}-%{release}

%description devel
Common Access Card (CAC) Emulation Development library

%prep
%setup -q -n qemu-%{version}

%build
#if build with clang, should enable it.
#--extra-cflags="$RPM_OPT_FLAGS -fno-integrated-as"
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir} \
            --extra-ldflags="$extraldflags -lrt"
            

make V=1 %{?_smp_mflags} libcacard

%install
rm -rf $RPM_BUILD_ROOT
make install-libcacard DESTDIR=$RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT/%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libcacard.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcacard.so
%{_libdir}/libcacard.a
%dir %{_includedir}/cacard
%{_includedir}/cacard/*

%changelog
* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 2.4.0
%{_includedir}/cacard/*
