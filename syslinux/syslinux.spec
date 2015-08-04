Summary: Kernel loader which uses a FAT, ext2/3 or iso9660 filesystem or a PXE network
Name: syslinux
Version: 6.03
Release: 1
License: GPL
Group: System/Boot
Source0: ftp://ftp.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.xz
Patch0001: 0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
# Backport from upstream git master to fix RHBZ #1234653
Patch0002: 0035-SYSAPPEND-Fix-space-stripping.patch

ExclusiveArch: i386 i486 i586 i686 athlon pentium4 x86_64
BuildRequires: nasm >= 2.03, perl
BuildRequires: gnu-efi-devel
Autoreq: 0
Requires: mtools

%package devel
Summary: Development environment for SYSLINUX add-on modules
Group: Development/Libraries
Requires: syslinux

%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%description devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.

%prep
%setup -q -n syslinux-%{version}
%patch0001 -p1
%patch0002 -p1
#drop efi32 build
sed -i 's/efi32:/drop:/g' Makefile
sed -i 's/efi32//g' Makefile

%build
make installer

%install
rm -rf %{buildroot}
make install \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING NEWS doc/*
%doc sample
%{_mandir}/man*/*
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/syslinux/*.com
%{_datadir}/syslinux/*.exe
%{_datadir}/syslinux/*.c32
%{_datadir}/syslinux/*.bin
%{_datadir}/syslinux/*.0
%{_datadir}/syslinux/memdisk
%{_datadir}/syslinux/dosutil/*
%{_datadir}/syslinux/diag/*
%{_datadir}/syslinux/efi64/*

%files devel
%{_datadir}/syslinux/com32

