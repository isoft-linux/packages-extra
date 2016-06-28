%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# Build ocaml bits unless rpmbuild was run with --without ocaml 
# or ocamlopt is missing (the xen makefile doesn't build ocaml bits if it isn't there)
#%define with_ocaml  %{?_without_ocaml: 0} %{?!_without_ocaml: 1}
%define with_ocaml 0
%define build_ocaml 0
#%define build_ocaml %(test -x %{_bindir}/ocamlopt && echo %{with_ocaml} || echo 0)
# build xsm support unless rpmbuild was run with --without xsm
# or required packages are missing
%define with_xsm  %{?_without_xsm: 0} %{?!_without_xsm: 1}
%define build_xsm %(test -x %{_bindir}/checkpolicy && test -x %{_bindir}/m4 && echo %{with_xsm} || echo 0)
# cross compile 64-bit hypervisor on ix86 unless rpmbuild was run
#	with --without crosshyp
%define build_crosshyp %{?_without_crosshyp: 0} %{?!_without_crosshyp: 1}
%ifnarch %{ix86}
%define build_crosshyp 0
%define build_hyp 1
%else
%if %build_crosshyp
%define build_hyp 1
%else
%define build_hyp 0
# no point in trying to build xsm on ix86 without a hypervisor
%define build_xsm 0
%endif
%endif
# build an efi boot image (where supported) unless rpmbuild was run with
# --without efi
%define build_efi %{?_without_efi: 0} %{?!_without_efi: 1}
# xen only supports efi boot images on x86_64
%ifnarch x86_64
%define build_efi 0
%endif
%if "%dist" >= ".fc17"
%define with_sysv 0
%else
%define with_sysv 1
%endif
%if "%dist" >= ".fc15"
%define with_systemd 1
%else
%define with_systemd 0
%endif
%if "%dist" >= ".fc20"
%define with_systemd_presets 1
%else
%define with_systemd_presets 0
%endif

%define with_sysv 0
%define build_efi 0
%define with_systemd 0

# Hypervisor ABI
%define hv_abi  4.5

Summary: Xen is a virtual machine monitor
Name:    xen
Version: 4.5.3
Release: 3
Group:   Development/Libraries
License: GPLv2+ and LGPLv2+ and BSD
URL:     http://xen.org/
Source0: http://bits.xensource.com/oss-xen/release/%{version}/xen-%{version}.tar.gz
Source1: %{name}.modules
Source2: %{name}.logrotate
# used by stubdoms
Source10: lwip-1.3.0.tar.gz
Source11: newlib-1.16.0.tar.gz
Source12: zlib-1.2.3.tar.gz
Source13: pciutils-2.2.9.tar.bz2
Source14: grub-0.97.tar.gz
Source15: polarssl-1.1.4-gpl.tgz
# init.d bits
Source20: init.xenstored
Source21: init.xenconsoled
# sysconfig bits
Source30: sysconfig.xenstored
Source31: sysconfig.xenconsoled

Patch4: xen-dumpdir.patch
Patch5: xen-net-disable-iptables-on-bridge.patch

Patch11: xen.use.fedora.ipxe.patch
Patch12: xen.fedora.efi.build.patch
Patch13: xen.xsm.enable.patch
Patch14: xen.64.bit.hyp.on.ix86.patch
Patch15: CVE-2014-0150.patch
Patch16: xen.fedora.systemd.patch
Patch17: xen.ocaml.uint.fix.patch
Patch18: xen.ocaml.selinux.fix.patch
Patch19: xen.gcc5.fix.patch
Patch20: qemu.trad.build.patch
Patch21: xen.fedora.crypt.patch
Patch22: qemu.trad.CVE-2015-6815.patch
Patch23: qemu.trad.CVE-2015-5279.patch
Patch24: qemu.trad.CVE-2015-5278.patch
Patch25: qemu.git-7882080388be5088e72c425b02223c02e6cb4295.patch
Patch26: qemu.git-d9033e1d3aa666c5071580617a57bd853c5d794a.patch
Patch27: qemu.git-ce317461573bac12b10d67699b4ddf1f97cf066c.patch
Patch28: qemu.git-29b9f5efd78ae0f9cc02dd169b6e80d2c404bade.patch
Patch29: qemu.git-0cf33fb6b49a19de32859e2cdc6021334f448fb3.patch
Patch30: qemu.git-00837731d254908a841d69298a4f9f077babaf24.patch
Patch31: qemu.trad.CVE-2015-8345.patch
Patch32: qemu.trad.CVE-2015-7512.patch
Patch33: qemu.trad.CVE-2015-8504.patch
Patch34: xsa155-xen-0001-xen-Add-RING_COPY_REQUEST.patch
Patch35: xsa155-xen-0002-blktap2-Use-RING_COPY_REQUEST.patch
Patch36: qemu.git-43b11a91dd861a946b231b89b754285.patch
Patch37: qemu.git-d9a3b33d2c9f996537b7f1d0246dee2d0120cefb.patch
Patch38: qemu.git-a7278b36fcab9af469563bd7b.patch
Patch39: qemu.git-c6048f849c7e3f009786df76206e895.patch
Patch40: qemu.trad.CVE-2016-1714.patch
Patch41: qemu.CVE-2016-1922.patch
Patch42: qemu.trad.CVE-2016-1981.patch
Patch43: qemu.CVE-2016-2198.patch
Patch44: qemu.CVE-2016-2841.patch
Patch45: qemu.trad.CVE-2016-2841.patch
Patch46: qemu.CVE-2016-2538.patch
Patch47: qemu.trad.CVE-2016-2538.patch
Patch48: qemu.CVE-2016-2392.patch
Patch49: qemu.CVE-2016-2391.patch
Patch50: qemu.CVE-2016-2857.patch
Patch51: qemu.trad.CVE-2016-2857.patch
Patch52: qemu.CVE-2015-8817+8.patch
Patch53: qemu.git-60253ed1e6ec6d8e5ef2efe7bf755f475.patch
Patch54: xsa172.patch
Patch55: xsa173-4.5.patch
Patch56: qemu.git-3a15cc0e1ee7168db0782133d2607a6bfa422d66.patch
Patch57: qemu.trad.CVE-2016-4001.patch
Patch58: qemu.CVE-2016-4002.patch
Patch59: qemu.trad.CVE-2016-4002.patch
Patch60: qemu.CVE-2016-4037.patch
Patch61: qemu.revert.CVE-2015-8558.patch
Patch62: tool-add-stubs-32.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libidn-devel zlib-devel texi2html SDL-devel curl-devel
#BuildRequires: transfig libidn-devel zlib-devel texi2html SDL-devel curl-devel
BuildRequires: libX11-devel python-devel ghostscript
#BuildRequires: libX11-devel python-devel ghostscript texlive-latex
%if "%dist" >= ".fc18"
BuildRequires: texlive-times texlive-courier texlive-helvetic texlive-ntgclass
%endif
BuildRequires: ncurses-devel gtk2-devel libaio-devel
# for the docs
BuildRequires: perl perl(Pod::Man) perl(Pod::Text) texinfo graphviz
# so that the makefile knows to install udev rules
BuildRequires: udev
%ifarch %{ix86} x86_64
# so that x86_64 builds pick up glibc32 correctly
#BuildRequires: /usr/include/gnu/stubs-32.h
# for the VMX "bios"
BuildRequires: dev86
%endif
BuildRequires: gettext
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
# For ioemu PCI passthrough
BuildRequires: pciutils-devel
# Several tools now use uuid
BuildRequires: libuuid-devel
# iasl needed to build hvmloader
BuildRequires: iasl
# build using Fedora seabios and ipxe packages for roms
BuildRequires: seabios-bin ipxe-roms-qemu
# modern compressed kernels
BuildRequires: bzip2-devel xz-devel
# libfsimage
BuildRequires: e2fsprogs-devel
# tools now require yajl and wget
BuildRequires: yajl-devel wget
# remus support now needs libnl3
BuildRequires: libnl3-devel
%if %with_xsm
# xsm policy file needs needs checkpolicy and m4
BuildRequires: checkpolicy m4
%endif
%if %build_crosshyp
# cross compiler for building 64-bit hypervisor on ix86
BuildRequires: gcc-x86_64-linux-gnu
%endif
Requires: bridge-utils
Requires: python-lxml
Requires: udev >= 059
Requires: xen-runtime = %{version}-%{release}
# Not strictly a dependency, but kpartx is by far the most useful tool right
# now for accessing domU data from within a dom0 so bring it in when the user
# installs xen.
#Requires: kpartx
#Requires: chkconfig
ExclusiveArch: %{ix86} x86_64
#ExclusiveArch: %#{ix86} x86_64 ia64 noarch
%if %with_ocaml
BuildRequires: ocaml, ocaml-findlib
%endif
# efi image needs an ld that has -mi386pep option
%if %build_efi
BuildRequires: mingw64-binutils
%endif
%if %with_systemd_presets
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%endif
%if %with_systemd
BuildRequires: systemd-devel
%endif

%description
This package contains the XenD daemon and xm command line
tools, needed to manage virtual machines running under the
Xen hypervisor

%package libs
Summary: Libraries for Xen tools
Group: Development/Libraries
Requires(pre): /sbin/ldconfig
Requires(post): /sbin/ldconfig
Requires: xen-licenses

%description libs
This package contains the libraries needed to run applications
which manage Xen virtual machines.


%package runtime
Summary: Core Xen runtime environment
Group: Development/Libraries
Requires: xen-libs = %{version}-%{release}
#Requires: /usr/bin/qemu-img /usr/bin/qemu-nbd
Requires: /usr/bin/qemu-img
# Ensure we at least have a suitable kernel installed, though we can't
# force user to actually boot it.
Requires: xen-hypervisor-abi = %{hv_abi}

%description runtime
This package contains the runtime programs and daemons which
form the core Xen userspace environment.


%package hypervisor
Summary: Libraries for Xen tools
Group: Development/Libraries
Provides: xen-hypervisor-abi = %{hv_abi}
Requires: xen-licenses

%description hypervisor
This package contains the Xen hypervisor


%package doc
Summary: Xen documentation
Group: Documentation
#BuildArch: noarch
Requires: xen-licenses

%description doc
This package contains the Xen documentation.


%package devel
Summary: Development libraries for Xen tools
Group: Development/Libraries
Requires: xen-libs = %{version}-%{release}
Requires: libuuid-devel

%description devel
This package contains what's needed to develop applications
which manage Xen virtual machines.


%package licenses
Summary: License files from Xen source
Group: Documentation

%description licenses
This package contains the license files from the source used
to build the xen packages.


%if %build_ocaml
%package ocaml
Summary: Ocaml libraries for Xen tools
Group: Development/Libraries
Requires: ocaml-runtime, xen-libs = %{version}-%{release}

%description ocaml
This package contains libraries for ocaml tools to manage Xen
virtual machines.


%package ocaml-devel
Summary: Ocaml development libraries for Xen tools
Group: Development/Libraries
Requires: xen-ocaml = %{version}-%{release}

%description ocaml-devel
This package contains libraries for developing ocaml tools to
manage Xen virtual machines.
%endif


%prep
%setup -q
%patch4 -p1
%patch5 -p1

%patch11 -p1
%patch12 -p1
%if %build_xsm
%patch13 -p1
%endif
%if %build_crosshyp
%patch14 -p1
%endif
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1

# stubdom sources
#cp -v %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} stubdom


%build
%if !%build_ocaml
%define ocaml_flags OCAML_TOOLS=n
%endif
%if %build_efi
%define efi_flags LD_EFI=/usr/x86_64-w64-mingw32/bin/ld
mkdir -p dist/install/boot/efi/efi/fedora
%endif
%if %(test -f /usr/share/seabios/bios-256k.bin && echo 1|| echo 0)
%define seabiosloc /usr/share/seabios/bios-256k.bin
%else
%define seabiosloc /usr/share/seabios/bios.bin
%endif
export XEN_VENDORVERSION="-%{release}"
export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} %{?efi_flags} prefix=/usr dist-xen
./configure --prefix=%{_prefix} --libdir=%{_libdir} --with-system-seabios=%{seabiosloc} --with-system-qemu=/usr/bin/qemu-system-i386
make %{?_smp_mflags} %{?ocaml_flags} prefix=/usr dist-tools
make                 prefix=/usr dist-docs
unset CFLAGS
#make %{?ocaml_flags} dist-stubdom


%install
rm -rf %{buildroot}
%if %build_ocaml
mkdir -p %{buildroot}%{_libdir}/ocaml/stublibs
%endif
%if %build_efi
mkdir -p %{buildroot}/boot/efi/efi/fedora
%endif
make DESTDIR=%{buildroot} %{?efi_flags}  prefix=/usr install-xen
make DESTDIR=%{buildroot} %{?ocaml_flags} prefix=/usr install-tools
make DESTDIR=%{buildroot} prefix=/usr install-docs
#make DESTDIR=%{buildroot} %{?ocaml_flags} prefix=/usr install-stubdom
%if %build_efi
mv %{buildroot}/boot/efi/efi %{buildroot}/boot/efi/EFI
%endif
%if %build_xsm
# policy file should be in /boot/flask
mkdir %{buildroot}/boot/flask
mv %{buildroot}/boot/xenpolicy* %{buildroot}/boot/flask
%else
rm -f %{buildroot}/boot/xenpolicy*
%endif

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f1.list

############ kill unwanted stuff ############

# stubdom: newlib
rm -rf %{buildroot}/usr/*-xen-elf

# hypervisor symlinks
rm -rf %{buildroot}/boot/xen-4.0.gz
rm -rf %{buildroot}/boot/xen-4.gz
%if !%build_hyp
rm -rf %{buildroot}/boot
%endif

# silly doc dir fun
rm -fr %{buildroot}%{_datadir}/doc/xen
rm -rf %{buildroot}%{_datadir}/doc/qemu

# Pointless helper
rm -f %{buildroot}%{_sbindir}/xen-python-path

# qemu stuff (unused or available from upstream)
rm -rf %{buildroot}/usr/share/xen/man
rm -rf %{buildroot}/usr/bin/qemu-*-xen
ln -s qemu-img %{buildroot}/%{_bindir}/qemu-img-xen
ln -s qemu-img %{buildroot}/%{_bindir}/qemu-nbd-xen
for file in bios.bin openbios-sparc32 openbios-sparc64 ppc_rom.bin \
         pxe-e1000.bin pxe-ne2k_pci.bin pxe-pcnet.bin pxe-rtl8139.bin \
         vgabios.bin vgabios-cirrus.bin video.x openbios-ppc bamboo.dtb
do
	rm -f %{buildroot}/%{_datadir}/xen/qemu/$file
done

# README's not intended for end users
rm -f %{buildroot}/%{_sysconfdir}/xen/README*

# standard gnu info files
rm -rf %{buildroot}/usr/info

# adhere to Static Library Packaging Guidelines
rm -rf %{buildroot}/%{_libdir}/*.a

%if %build_efi
# clean up extra efi files
rm -rf %{buildroot}/%{_libdir}/efi
%endif

############ fixup files in /etc ############

# udev
#rm -rf %{buildroot}/etc/udev/rules.d/xen*.rules
#mv %{buildroot}/etc/udev/xen*.rules %{buildroot}/etc/udev/rules.d

# modules
%if %with_sysv
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/modules/%{name}.modules
%endif

# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# init scripts
#mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
#mv %{buildroot}%{_sysconfdir}/init.d/* %{buildroot}%{_sysconfdir}/rc.d/init.d
#rmdir %{buildroot}%{_sysconfdir}/init.d
%if %with_sysv
install -m 755 %{SOURCE20} %{buildroot}%{_sysconfdir}/rc.d/init.d/xenstored
install -m 755 %{SOURCE21} %{buildroot}%{_sysconfdir}/rc.d/init.d/xenconsoled
%else
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xen-watchdog
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xencommons
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xendomains
%endif

# sysconfig
%if %with_sysv
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE30} %{buildroot}%{_sysconfdir}/sysconfig/xenstored
install -m 644 %{SOURCE31} %{buildroot}%{_sysconfdir}/sysconfig/xenconsoled
%endif

############ create dirs in /var ############

mkdir -p %{buildroot}%{_localstatedir}/lib/xen/images
mkdir -p %{buildroot}%{_localstatedir}/log/xen/console

############ create symlink for x86_64 for compatibility with 4.4 ############

%if "%{_libdir}" != "/usr/lib"
ln -s /usr/lib/%{name} %{buildroot}/%{_libdir}/%{name}
%endif

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f2.list
diff -u f1.list f2.list || true

############ assemble license files ############

mkdir licensedir
# avoid licensedir to avoid recursion, also stubdom/ioemu and dist
# which are copies of files elsewhere
find . -path licensedir -prune -o -path stubdom/ioemu -prune -o \
  -path dist -prune -o -name COPYING -o -name LICENSE | while read file; do
  mkdir -p licensedir/`dirname $file`
  install -m 644 $file licensedir/$file
done

############ all done now ############

%post
%if %with_sysv
/sbin/chkconfig --add xendomains
%endif
%if %with_systemd
%if %with_systemd_presets
%systemd_post xendomains.service
%else
if [ $1 == 1 ]; then
  /bin/systemctl enable xendomains.service
fi
%endif
%endif

%preun
%if %with_systemd_presets
%systemd_preun xendomains.service
%else
if [ $1 == 0 ]; then
%if %with_sysv
  /sbin/chkconfig --del xendomains
%endif
%if %with_systemd
/bin/systemctl disable xendomains.service
%endif
fi
%endif

%if %with_systemd_presets
%postun
%systemd_postun
%endif

%post runtime
%if %with_sysv
/sbin/chkconfig --add xenconsoled
/sbin/chkconfig --add xenstored
%endif
%if %with_systemd
%if %with_systemd_presets
%systemd_post xenstored.service xenconsoled.service
%else
if [ $1 == 1 ]; then
  /bin/systemctl enable xenstored.service
  /bin/systemctl enable xenconsoled.service
fi
%endif
%endif

%if %with_sysv
if [ $1 != 0 ]; then
  service xenconsoled condrestart
fi
%endif

%preun runtime
%if %with_systemd_presets
%systemd_preun xenstored.service xenconsoled.service
%else
if [ $1 == 0 ]; then
%if %with_sysv
  /sbin/chkconfig --del xenconsoled
  /sbin/chkconfig --del xenstored
%endif
%if %with_systemd
  /bin/systemctl disable xenstored.service
  /bin/systemctl disable xenconsoled.service
%endif
fi
%endif

%if %with_systemd_presets
%postun runtime
%systemd_postun
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%if %build_hyp
%post hypervisor
if [ $1 == 1 -a -f /sbin/grub2-mkconfig ]; then
  if [ -f /boot/grub2/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/grub2/grub.cfg
  fi
  if [ -f /boot/efi/EFI/fedora/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg
  fi
fi

%postun hypervisor
if [ -f /sbin/grub2-mkconfig ]; then
  if [ -f /boot/grub2/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/grub2/grub.cfg
  fi
  if [ -f /boot/efi/EFI/fedora/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg
  fi
fi
%endif

%if %build_ocaml
%post ocaml
%if %with_systemd
%if %with_systemd_presets
%systemd_post oxenstored.service
%else
if [ $1 == 1 ]; then
  /bin/systemctl enable oxenstored.service
fi
%endif
%endif

%preun ocaml
%if %with_systemd
%if %with_systemd_presets
%systemd_preun oxenstored.service
%else
if [ $1 == 0 ]; then
  /bin/systemctl disable oxenstored.service
fi
%endif
%endif

%if %with_systemd_presets
%postun ocaml
%systemd_postun
%endif
%endif

%clean
rm -rf %{buildroot}

# Base package only contains XenD/xm python stuff
#files -f xen-xm.lang
%files
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/xencons
%{python_sitearch}/%{name}
%{python_sitearch}/xen-*.egg-info

# Startup script
%if %with_sysv
%{_sysconfdir}/rc.d/init.d/xendomains
%endif
# Guest autostart links
%dir %attr(0700,root,root) %{_sysconfdir}/%{name}/auto
# Autostart of guests
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains

%if %with_systemd
%{_unitdir}/xendomains.service
%endif

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/fs

# All runtime stuff except for XenD/xm python stuff
%files runtime
%defattr(-,root,root)
# Hotplug rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/*

%dir %attr(0700,root,root) %{_sysconfdir}/%{name}
%dir %attr(0700,root,root) %{_sysconfdir}/%{name}/scripts/
%config %attr(0700,root,root) %{_sysconfdir}/%{name}/scripts/*

%if %with_sysv
%{_sysconfdir}/rc.d/init.d/xenstored
%{_sysconfdir}/rc.d/init.d/xenconsoled
%{_sysconfdir}/rc.d/init.d/xen-watchdog
%{_sysconfdir}/rc.d/init.d/xencommons
%endif
%{_sysconfdir}/bash_completion.d/xl.sh

%if %with_systemd
%{_unitdir}/proc-xen.mount
%{_unitdir}/var-lib-xenstored.mount
%{_unitdir}/xenstored.service
%{_unitdir}/xenconsoled.service
%{_unitdir}/xen-watchdog.service
%{_unitdir}/xen-qemu-dom0-disk-backend.service
%{_unitdir}/xenstored.socket
%{_unitdir}/xenstored_ro.socket
/usr/lib/modules-load.d/xen.conf
%endif

%if %with_sysv
%config(noreplace) %{_sysconfdir}/sysconfig/xenstored
%config(noreplace) %{_sysconfdir}/sysconfig/xenconsoled
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/xencommons
%config(noreplace) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xlexample*

# Auto-load xen backend drivers
%if %with_sysv
%attr(0755,root,root) %{_sysconfdir}/sysconfig/modules/%{name}.modules
%endif

# Rotate console log files
%config(noreplace) %{_sysconfdir}/logrotate.d/xen

# Programs run by other programs
%dir /usr/lib/%{name}
%dir /usr/lib/%{name}/bin
%attr(0700,root,root) /usr/lib/%{name}/bin/*
# QEMU runtime files
%dir %{_datadir}/%{name}/qemu
%dir %{_datadir}/%{name}/qemu/keymaps
%{_datadir}/%{name}/qemu/keymaps/*

# man pages
%{_mandir}/man1/xentop.1*
%{_mandir}/man1/xentrace_format.1*
%{_mandir}/man8/xentrace.8*
%{_mandir}/man1/xl.1*
%{_mandir}/man5/xl.cfg.5*
%{_mandir}/man5/xl.conf.5*
%{_mandir}/man5/xlcpupool.cfg.5*
%{_mandir}/man1/xenstore*

%{python_sitearch}/fsimage.so
%{python_sitearch}/grub
%{python_sitearch}/pygrub-*.egg-info

# The firmware
%ifarch %{ix86} x86_64
%dir /usr/lib/%{name}/boot
%if "%{_libdir}" != "/usr/lib"
%{_libdir}/%{name}
%endif
/usr/lib/xen/boot/hvmloader
#/usr/lib/xen/boot/ioemu-stubdom.gz
#/usr/lib/xen/boot/xenstore-stubdom.gz
#/usr/lib/xen/boot/pv-grub*.gz
%endif
# General Xen state
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/dump
%dir %{_localstatedir}/lib/%{name}/images
# Xenstore persistent state
%dir %{_localstatedir}/lib/xenstored
# Xenstore runtime state
%ghost %{_localstatedir}/run/xenstored

# All xenstore CLI tools
%{_bindir}/qemu-*-xen
%{_bindir}/xenstore
%{_bindir}/xenstore-*
%{_bindir}/pygrub
%{_bindir}/xentrace*
#%#{_bindir}/remus
# blktap daemon
%{_sbindir}/tapdisk*
# XSM
%if %build_xsm
%{_sbindir}/flask-*
%endif
# Disk utils
%{_sbindir}/qcow-create
%{_sbindir}/qcow2raw
%{_sbindir}/img2qcow
# Misc stuff
%{_bindir}/xen-detect
%{_bindir}/xencov_split
%{_sbindir}/gdbsx
%{_sbindir}/gtrace*
%{_sbindir}/kdd
%{_sbindir}/lock-util
%{_sbindir}/tap-ctl
%{_sbindir}/td-util
%{_sbindir}/vhd-*
%{_sbindir}/xen-bugtool
%{_sbindir}/xen-hptool
%{_sbindir}/xen-hvmcrash
%{_sbindir}/xen-hvmctx
%{_sbindir}/xen-tmem-list-parse
%{_sbindir}/xenconsoled
%{_sbindir}/xenlockprof
%{_sbindir}/xenmon.py*
%{_sbindir}/xentop
%{_sbindir}/xentrace_setmask
%{_sbindir}/xenbaked
%{_sbindir}/xenstored
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_sbindir}/xenperf
%{_sbindir}/xenwatchdogd
%{_sbindir}/xl
%{_sbindir}/xen-lowmemd
%{_sbindir}/xen-ringwatch
%{_sbindir}/xencov
%{_sbindir}/xen-mfndump

# Xen logfiles
%dir %attr(0700,root,root) %{_localstatedir}/log/xen
# Guest/HV console logs
%dir %attr(0700,root,root) %{_localstatedir}/log/xen/console

%files hypervisor
%if %build_hyp
%defattr(-,root,root)
/boot/xen-syms-*
/boot/xen-*.gz
/boot/xen.gz
%if %build_xsm
%dir %attr(0755,root,root) /boot/flask
/boot/flask/xenpolicy*
%endif
%if %build_efi
/boot/efi/EFI/fedora/*.efi
%endif
%endif

%files doc
%defattr(-,root,root)
%doc docs/misc/
%doc dist/install/usr/share/doc/xen/html

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%dir %{_includedir}/xen
%{_includedir}/xen/*
%dir %{_includedir}/xenstore-compat
%{_includedir}/xenstore-compat/*
%{_libdir}/*.so

%files licenses
%defattr(-,root,root)
%doc licensedir/*

%if %build_ocaml
%files ocaml
%defattr(-,root,root)
%{_libdir}/ocaml/xen*
%exclude %{_libdir}/ocaml/xen*/*.a
%exclude %{_libdir}/ocaml/xen*/*.cmxa
%exclude %{_libdir}/ocaml/xen*/*.cmx
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%{_sbindir}/oxenstored
%config(noreplace) %{_sysconfdir}/xen/oxenstored.conf
%{_unitdir}/oxenstored.service

%files ocaml-devel
%defattr(-,root,root)
%{_libdir}/ocaml/xen*/*.a
%{_libdir}/ocaml/xen*/*.cmxa
%{_libdir}/ocaml/xen*/*.cmx
%endif

%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 4.5.3-3
- rebuilt for libvirt

