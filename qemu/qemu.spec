#this package use internal rom shiped with qemu

%define _udevdir %{_libdir}/udev/rules.d


Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 2.5.0
Release: 5
License: GPLv2+ and LGPLv2+ and BSD
URL: http://www.qemu.org/

Source0: qemu-%{version}-rc2.tar.bz2

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


BuildRequires: SDL2-devel
BuildRequires: zlib-devel
BuildRequires: which
BuildRequires: chrpath
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: usbredir-devel >= 0.5.2
%ifnarch s390 s390x
BuildRequires: gperftools-devel
%endif
BuildRequires: texinfo
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: libspice-devel
# For network block driver
BuildRequires: libcurl-devel
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For smartcard NSS support
BuildRequires: nss-devel
# For XFS discard support in raw-posix.c
BuildRequires: xfsprogs-devel
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusb-devel
# SSH block driver
BuildRequires: libssh2-devel
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte3-devel
# GTK translations
BuildRequires: gettext
# For acpi compilation/iasl
BuildRequires: acpica-tools 
# memdev hostmem backend added in 2.1
%ifarch %{ix86} x86_64 aarch64
BuildRequires: numactl-devel
%endif
# Added in qemu 2.3
BuildRequires: bzip2-devel
# Added in qemu 2.4 for opengl bits
BuildRequires: libepoxy-devel

#it's now a standalone project.
BuildRequires: libcacard-devel

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
%setup -q -n qemu-%{version}-rc2

%build
buildarch="i386-softmmu x86_64-softmmu alpha-softmmu arm-softmmu \
cris-softmmu lm32-softmmu m68k-softmmu microblaze-softmmu \
microblazeel-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
mips64el-softmmu or32-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu \
s390x-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
xtensa-softmmu xtensaeb-softmmu unicore32-softmmu moxie-softmmu \
tricore-softmmu \
i386-linux-user x86_64-linux-user aarch64-linux-user alpha-linux-user \
arm-linux-user armeb-linux-user cris-linux-user m68k-linux-user \
microblaze-linux-user microblazeel-linux-user mips-linux-user \
mipsel-linux-user mips64-linux-user mips64el-linux-user \
mipsn32-linux-user mipsn32el-linux-user \
or32-linux-user ppc-linux-user ppc64-linux-user ppc64le-linux-user \
ppc64abi32-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user \
sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
unicore32-linux-user aarch64-softmmu"

./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir} \
    --localstatedir=%{_localstatedir} \
    --libexecdir=%{_libexecdir} \
    --target-list="$buildarch" \
    --audio-drv-list=pa,sdl,alsa \
    --enable-pie \
    --disable-werror \
    --enable-spice \
    --enable-virtfs \
    --enable-vnc \
    --enable-kvm \
    --enable-libusb \
    --enable-usb-redir \
    --enable-smartcard \
    --disable-strip \
    --disable-xen \
    --disable-vnc-sasl \
    --enable-sdl \
    --with-sdlabi="2.0" \
    --with-gtkabi="3.0"
            

make V=1 %{?_smp_mflags} $buildldflags

cc %{SOURCE6} -O2 -g -o ksmctl

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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

#find_lang qemu
#remove translations
rm -rf %{buildroot}%{_datadir}/locale

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
%attr(4755, root, root) %{_libexecdir}/qemu-bridge-helper
%dir %{_docdir}/qemu
%{_docdir}/qemu/*
%{_mandir}/man?/*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*

%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 2.5.0-5
- Remove qemu-i386 userspace binfmt support

* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 2.5.0-4
- Update to rc2

* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 2.5.0-3
- Update to qemu 2.5.0rc0

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.4.0-2
- Rebuild

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 2.4.0
* Sun Aug 09 2015 Cjacker <cjacker@foxmail.com>
- update to 2.4.0-rc4
