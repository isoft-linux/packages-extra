%define qemu_user  root
%define qemu_group root

Name:          libvirt
Version:       1.3.3
Release:       1
Summary:       Virtualization API
URL:           http://libvirt.org
Source0:       http://libvirt.org/sources/libvirt-%{version}.tar.gz
License:       LGPL

# libvirt assigns same address to two PCI devices (bz #1325085)
Patch0: 0001-qemu-support-virt-2.6-machine-type-on-arm.patch
# Fix build with -Werror
Patch1: 0002-build-cleanup-GCC-4.6-Wlogical-op-workaround.patch
Patch2: 0003-build-add-GCC-6.0-Wlogical-op-workaround.patch

# Fix 200ms performance problem when waiting for monitor socket of
# new domains.
# Upstream commit beaa447a2982bc78adb26c183560d0ee566c1268.
Patch3: 0001-Add-functions-for-handling-exponential-backoff-loops.patch

BuildRequires: glibc-devel
BuildRequires: avahi-devel
BuildRequires: libblkid-devel
#BuildRequires: libcares-devel
BuildRequires: libcurl-devel
BuildRequires: dbus-devel
BuildRequires: device-mapper-devel
BuildRequires: e2fsprogs-devel
BuildRequires: libgcrypt-devel
BuildRequires: gnutls-devel
BuildRequires: libgpg-error-devel
BuildRequires: libidn-devel
BuildRequires: krb5-devel
BuildRequires: ncurses-devel
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: parted-devel
BuildRequires: python-devel
BuildRequires: readline-devel
BuildRequires: cyrus-sasl-devel
#BuildRequires: selinux-devel
#BuildRequires: sepol-devel
#BuildRequires: smbios-devel
BuildRequires: libssh2-devel
#BuildRequires: ssp-devel
BuildRequires: libstdc++-devel
BuildRequires: libtasn1-devel
BuildRequires: libuuid-devel
BuildRequires: libxml2-devel
BuildRequires: libzip-devel

#BuildRequires: libyajl-devel
BuildRequires: libpcap-devel >= 1.2
BuildRequires: systemtap-sdt-devel
BuildRequires: systemd-devel
BuildRequires: libpciaccess-devel
BuildRequires: libnl3-devel

Requires:      dnsmasq
Requires:      ebtables
Requires:      netcat-openbsd
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
Libvirt is a C toolkit to interact with the virtualization capabilities of recent versions of Linux (and other OSes).

%package client
Summary:       Client side library and utilities of the libvirt library

%description client
Shared libraries and client binaries needed to access to the virtualization capabilities of recent versions of Linux (and other OSes).

%package -n python-%{name}
Summary:       Python bindings for the libvirt library
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description -n python-%{name}
The libvirt-python package contains a module that permits applications written in the Python programming language to use the interface supplied by the libvirt library to use the virtualization capabilities of recent versions of Linux (and other OSes).

%package devel
Summary:       Static libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
Libvirt is a C toolkit to interact with the virtualization capabilities of recent versions of Linux (and other OSes).
This package contains static libraries and header files need for development.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
autoreconf -if
%configure \
   --without-xen \
   --with-systemd-daemon \
   --with-init-script=systemd \
   --with-qemu-user=%{qemu_user} \
   --with-qemu-group=%{qemu_group} \
   --without-wireshark-dissector
make %{?_smp_mflags}

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
make install DESTDIR=%{?buildroot} SYSTEMD_UNIT_DIR=%{_unitdir}

install -d %{buildroot}%{_localstatedir}/log/libvirt/{lxc,uml,qemu}

install -d %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d

cat > %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-org.libvirt.unix.manage.pkla << _EOF
[Allow group libvirt management permissions]
Identity=unix-group:sysadmin
Action=org.libvirt.unix.manage
ResultAny=yes
ResultInactive=yes
ResultActive=yes
_EOF

%find_lang %{name}

rm -fr %{buildroot}%{_datadir}/doc/libvirt-%{version}
rm -fr %{buildroot}%{_datadir}/doc/libvirt-python-%{version}

rm -f %{buildroot}%{_libdir}/*.a

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%post
if [ $1 -ge 1 ]; then
   systemctl -q daemon-reload
   systemctl -q enable libvirtd
fi
exit 0

%preun
if [ $1 -eq 0 ]; then
   systemctl -q disable libvirtd
fi
exit 0

%postun
if [ $1 -ge 1 ]; then
   systemctl -q daemon-reload
fi
exit 0

%post client
if [ $1 -ge 1 ]; then
   systemctl -q daemon-reload
   /sbin/ldconfig
fi
:

%postun client
if [ $1 -eq 0 ]; then
   systemctl -q daemon-reload
   /sbin/ldconfig
fi
:

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/libvirt/libvirt.conf
%dir %{_sysconfdir}/libvirt
%dir %{_sysconfdir}/libvirt/qemu
%dir %{_sysconfdir}/libvirt/qemu/networks
%{_sysconfdir}/libvirt/qemu/networks/default.xml
%dir %{_sysconfdir}/libvirt/qemu/networks/autostart
%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
%{_sysconfdir}/libvirt/nwfilter
%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-org.libvirt.unix.manage.pkla
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/libvirt/libvirt-admin.conf
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virt-login-shell.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtlockd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtlogd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.*
%config(noreplace) %{_sysconfdir}/sysconfig/virtlockd
%config(noreplace) %{_sysconfdir}/sysconfig/virtlogd
%{_bindir}/virt-admin
%{_bindir}/virt-host-validate
%{_bindir}/virt-login-shell
%{_sbindir}/libvirtd
%{_sbindir}/virtlockd
%{_sbindir}/virtlogd
%{_unitdir}/libvirtd.service
%{_unitdir}/libvirtd.socket
%{_unitdir}/virtlockd.service
%{_unitdir}/virtlockd.socket
%{_unitdir}/virtlogd.service
%{_unitdir}/virtlogd.socket
%dir %{_datadir}/libvirt
%dir %{_datadir}/libvirt/api
%{_datadir}/libvirt/api/libvirt-api.xml
%{_datadir}/libvirt/api/libvirt-lxc-api.xml
%{_datadir}/libvirt/libvirtLogo.png
%{_datadir}/augeas/lenses/*.aug
%{_datadir}/augeas/lenses/tests/test_*.aug
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%{_datadir}/polkit-1/rules.d/50-libvirt.rules
%{_datadir}/systemtap/tapset/libvirt_*.stp
%dir %{_localstatedir}/log/libvirt
%dir %{_localstatedir}/log/libvirt/lxc
%dir %{_localstatedir}/log/libvirt/uml
%dir %{_localstatedir}/log/libvirt/qemu
%{_mandir}/man1/virt-admin.1*
%{_mandir}/man1/virt-host-validate.1*
%{_mandir}/man1/virt-login-shell.1*
%{_mandir}/man8/libvirtd.8*
%{_mandir}/man8/virtlockd.8*
%{_mandir}/man8/virtlogd.8*
%{_datadir}/libvirt/api/libvirt-qemu-api.xml
%doc AUTHORS COPYING.LESSER

%files client -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%{_unitdir}/libvirt-guests.service
%{_sysconfdir}/sysconfig/libvirt-guests
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
%{_bindir}/virt-pki-validate
%{_libdir}/lib*.so.*
%dir %{_libdir}/libvirt
%dir %{_libdir}/libvirt/connection-driver
%{_libdir}/libvirt/connection-driver/libvirt_driver_interface.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_interface.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_network.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_network.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_secret.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_secret.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_storage.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_storage.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_uml.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_uml.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox.la
%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox.so
#%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox_network.la
#%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox_network.so
#%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox_storage.la
#%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox_storage.so
%dir %{_libdir}/libvirt/lock-driver
%{_libdir}/libvirt/lock-driver/lockd.la
%{_libdir}/libvirt/lock-driver/lockd.so
%{_prefix}/lib/sysctl.d/60-libvirtd.conf
%{_libexecdir}/libvirt_lxc
%{_libexecdir}/libvirt_iohelper
%{_libexecdir}/libvirt_leaseshelper
%{_libexecdir}/libvirt_parthelper
%{_libexecdir}/libvirt-guests.sh
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%dir %{_datadir}/libvirt
%{_datadir}/libvirt/cpu_map.xml
%{_datadir}/libvirt/schemas/*.rng
%{_mandir}/man1/virsh.*
%{_mandir}/man1/virt-xml-validate.*
%{_mandir}/man1/virt-pki-validate.*
#%doc COPYING

%files devel
%defattr(-,root,root)
%{_libdir}/*.la
%{_libdir}/lib*.so
%{_includedir}/libvirt/*.h
%dir %{_datadir}/gtk-doc/html/libvirt
%{_datadir}/gtk-doc/html/libvirt/*
%{_libdir}/pkgconfig/libvirt.pc
%{_libdir}/pkgconfig/libvirt-lxc.pc
%{_libdir}/pkgconfig/libvirt-qemu.pc
#%doc docs/*.html docs/*.gif docs/*.png docs/html
#%doc docs/libvirt-api.xml
#%doc ChangeLog NEWS README TODO

%changelog
* Wed Apr 20 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> 1.3.3-1
- 1.3.3
