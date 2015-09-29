#this package use internal rom shiped with qemu

%define _udevdir %{_libdir}/udev/rules.d

Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 2.4.0
Release: 1
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/

Source0: qemu-%{version}.tar.bz2

Source1: qemu-kvm.sh

#a preset simple wrapper to enable user-mode network and ac97 soundcard
Source2: qemu-kvm-simple.sh
Source3: qemu-kvm-spice.sh


# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf

Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules

# Creates /dev/kvm
Source15: 80-kvm.rules

Source20: qemu.binfmt

BuildRequires: SDL-devel zlib-devel which
BuildRequires: libaio-devel
BuildRequires: pciutils-devel
BuildRequires: ncurses-devel
BuildRequires: spice-protocol
BuildRequires: libspice-devel
BuildRequires: usbredir-devel
BuildRequires: nss-devel nspr-devel glib2-devel

%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.

%prep
%setup -q -n qemu-%{version}

%build
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
            --localstatedir=%{_localstatedir} \
            --libexecdir=%{_libexecdir} \
            --target-list=x86_64-softmmu \
            --audio-drv-list=pa,alsa \
            --enable-spice \
            --disable-gtk \
            --enable-sdl \
            --enable-virtfs \
            --enable-vnc \
            --enable-kvm \
            --enable-libusb \
            --enable-usb-redir \
            --disable-strip \
            --disable-xen \
            --disable-vnc-sasl
            

make V=1 %{?_smp_mflags} $buildldflags

cc %{SOURCE6} -O2 -g -o ksmctl

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#remove libcacard.
rm -rf $RPM_BUILD_ROOT%{_libdir}/libcacard.*
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libcacard.*
rm -rf $RPM_BUILD_ROOT%{_includedir}/cacard


#fix perms
chmod +x $RPM_BUILD_ROOT/%{_libdir}/*
strip $RPM_BUILD_ROOT/%{_bindir}/*

#install qemu-kvm wrapper scripts
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/qemu-kvm
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/qemu-kvm-simple
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/qemu-kvm-spice


mkdir -p $RPM_BUILD_ROOT%{_udevdir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

install -m 0755 scripts/kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/

install -m 0644 %{SOURCE15} $RPM_BUILD_ROOT%{_udevdir}



install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT/%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT/%{_libdir}/systemd/ksmctl

install -D -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT/%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf



install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_udevdir}

# Install the usb redir config files, needed by qemu-kvm-spice wrapper
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/qemu/
install -m 0644 docs/ich9-ehci-uhci.cfg $RPM_BUILD_ROOT%{_sysconfdir}/qemu/
install -m 0644 docs/q35-chipset.cfg $RPM_BUILD_ROOT%{_sysconfdir}/qemu/

#setup binfmt.d
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/binfmt.d
for i in dummy \
    qemu-i386 \
    qemu-alpha \
    qemu-arm \
    qemu-armeb \
    qemu-mips qemu-mips64 \
    qemu-mipsel qemu-mips64el \
; do
  test $i = dummy && continue
  grep /$i:\$ %{SOURCE20} > $RPM_BUILD_ROOT/%{_libdir}/binfmt.d/$i.conf
  chmod 644 $RPM_BUILD_ROOT/%{_libdir}/binfmt.d/$i.conf
done < %{SOURCE20}

#remove not-necessary la file
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu
%systemd_post ksm.service
%systemd_post ksmtuned.service

%preun 
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun 
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service


%files
%defattr(-,root,root)
%{_sysconfdir}/ksmtuned.conf
%dir %{_sysconfdir}/qemu
%{_sysconfdir}/qemu/*
%{_sysconfdir}/sysconfig/ksm

%{_bindir}/*
%{_sbindir}/ksmtuned

%{_libdir}/systemd/ksmctl
%{_libdir}/udev/rules.d/*.rules
%{_libdir}/binfmt.d/*
%{_libdir}/systemd/system/ksm.service
%{_libdir}/systemd/system/ksmtuned.service
%{_libdir}/systemd/system/qemu-guest-agent.service
%{_libexecdir}/qemu-bridge-helper
%dir %{_docdir}/qemu
%{_docdir}/qemu/*
%{_mandir}/man?/*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*
#%{_datadir}/locale/*

%changelog
* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 2.4.0
* Sun Aug 09 2015 Cjacker <cjacker@foxmail.com>
- update to 2.4.0-rc4
