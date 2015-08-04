#it's part of qemu, since spice need libcacard and qemu need spice library.
#here seperate it.

%define _udevdir /usr/lib/udev/rules.d

Summary: Common Access Card (CAC) Emulation Development library
Name:    libcacard 
Version: 2.3.0
Release: 1 
License: GPLv2+ and LGPLv2+ and BSD
Group:   App/Runtime/Library
URL: http://www.qemu.org/
Source0: qemu-%{version}.tar.bz2

BuildRequires: SDL2-devel zlib-devel which
BuildRequires: libaio-devel
BuildRequires: pciutils-devel
BuildRequires: ncurses-devel
BuildRequires: spice-protocol
BuildRequires: usbredir-devel

%description
Common Access Card (CAC) Emulation

%package devel
Summary:   CAC Emulation devel
Group:     App/Development/Library
Requires:  libcacard = %{version}-%{release}

%description devel
Common Access Card (CAC) Emulation Development library



%prep
%setup -q -n qemu-%{version}

%build
export CC=clang
export CXX=clang++
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir} \
            --libexecdir=%{_libexecdir} \
            --target-list=x86_64-softmmu \
            --audio-drv-list=pa,alsa \
            --disable-spice \
            --enable-gtk \
            --disable-sdl \
            --enable-virtfs \
            --enable-vnc \
            --enable-kvm \
            --enable-libusb \
            --enable-usb-redir \
            --disable-strip \
            --disable-xen \
            --disable-gtk \
            --disable-vnc-sasl \
            --extra-ldflags="$extraldflags -lrt" \
            --extra-cflags="$RPM_OPT_FLAGS -fno-integrated-as"
            

make V=1 %{?_smp_mflags} libcacard

%install
rm -rf $RPM_BUILD_ROOT
make install-libcacard DESTDIR=$RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT/%{_libdir}/*
rpmclean

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
