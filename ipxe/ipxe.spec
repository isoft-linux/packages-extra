
# Resulting binary formats we want from iPXE
%global formats rom

# PCI IDs (vendor,product) of the ROMS we want for QEMU
#
#    pcnet32: 0x1022 0x2000
#   ne2k_pci: 0x10ec 0x8029
#      e1000: 0x8086 0x100e
#    rtl8139: 0x10ec 0x8139
# virtio-net: 0x1af4 0x1000
%global qemuroms 10222000 10ec8029 8086100e 10ec8139 1af41000

# We only build the ROMs if on an x86 build host. The resulting
# binary RPM will be noarch, so other archs will still be able
# to use the binary ROMs.
#
# We do cross-compilation for 32->64-bit, but not for other arches
# because EDK II does not support big-endian hosts.
%global buildarches %{ix86} x86_64

# debugging firmwares does not go the same way as a normal program.
# moreover, all architectures providing debuginfo for a single noarch
# package is currently clashing in koji, so don't bother.
%global debug_package %{nil}

# Upstream don't do "releases" :-( So we're going to use the date
# as the version, and a GIT hash as the release. Generate new GIT
# snapshots using the folowing commands:
#
# $ hash=`git log -1 --format='%h'`
# $ date=`git log -1 --format='%cd' --date=short | tr -d -`
# $ git archive --prefix ipxe-${date}-git${hash}/ ${hash} | xz -7e > ipxe-${date}-git${hash}.tar.xz
#
# And then change these two:

%global date 20150407
%global hash dc795b9f

Name:    ipxe
Version: %{date}
Release: 4.git%{hash}
Summary: A network boot loader

Group:   System Environment/Base
License: GPLv2 with additional permissions and BSD
URL:     http://ipxe.org/

Source0: %{name}-%{version}-git%{hash}.tar.xz
Source1: USAGE
Source2: config.local.general.h

# From upstream commit b12b1b620fffc89e86af3879a945e7ffaa7c141d
Patch0001: 0001-virtio-Downgrade-per-iobuf-debug-messages-to-DBGC2.patch
# From upstream commit 755d2b8f6be681a2e620534b237471b75f28ed8c
Patch0002: 0002-efi-Ensure-drivers-are-disconnected-when-ExitBootSer.patch

# From QEMU
Patch1001: qemu-0001-efi_snp-improve-compliance-with-the-EFI_SIMPLE_NETWO.patch
Patch1002: qemu-0002-efi-make-load-file-protocol-optional.patch

%ifarch %{buildarches}
BuildRequires: perl
BuildRequires: syslinux
BuildRequires: mtools
#BuildRequires: mkisofs
BuildRequires: /usr/bin/mkisofs
BuildRequires: zlib-devel
BuildRequires: edk2-tools
BuildRequires: xz-devel

BuildRequires: binutils-devel
#BuildRequires: binutils-x86_64-linux-gnu gcc-x86_64-linux-gnu


Obsoletes: gpxe <= 1.0.1

%package bootimgs
Summary: Network boot loader images in bootable USB, CD, floppy and GRUB formats
Group:   Development/Tools
BuildArch: noarch
Obsoletes: gpxe-bootimgs <= 1.0.1

%package roms
Summary: Network boot loader roms in .rom format
Group:  Development/Tools
Requires: %{name}-roms-qemu = %{version}-%{release}
BuildArch: noarch
Obsoletes: gpxe-roms <= 1.0.1

%package roms-qemu
Summary: Network boot loader roms supported by QEMU, .rom format
Group:  Development/Tools
BuildArch: noarch
Obsoletes: gpxe-roms-qemu <= 1.0.1

%description bootimgs
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE boot images in USB, CD, floppy, and PXE
UNDI formats.

%description roms
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE roms in .rom format.


%description roms-qemu
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE ROMs for devices emulated by QEMU, in
.rom format.
%endif

%description
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

%prep
%setup -q -n %{name}-%{version}-git%{hash}

# From upstream
%patch0001 -p1
%patch0002 -p1
# From QEMU
%patch1001 -p1
%patch1002 -p1

cp -a %{SOURCE1} .

# Apply local configuration tweaks
cp -a %{SOURCE2} src/config/local/general.h

%build
%ifarch %{buildarches}
# The src/Makefile.housekeeping relies on .git/index existing
# but since we pass GITVERSION= to make, we don't actally need
# it to be the real deal, so just touch it to let the build pass
mkdir .git
touch .git/index

ISOLINUX_BIN=/usr/share/syslinux/isolinux.bin
cd src
# ath9k drivers are too big for an Option ROM
rm -rf drivers/net/ath/ath9k

make %{?_smp_mflags} \
    bin/undionly.kpxe bin/ipxe.{dsk,iso,usb,lkrn} allroms \
    ISOLINUX_BIN=${ISOLINUX_BIN} NO_WERROR=1 V=1 \
    GITVERSION=%{hash} \
    CROSS_COMPILE=""

#    CROSS_COMPILE=x86_64-linux-gnu-

# build roms with efi support for qemu
mkdir bin-combined
for rom in %qemuroms; do
  make NO_WERROR=1 V=1 GITVERSION=%{hash} CROSS_COMPILE="" bin/${rom}.rom
  make NO_WERROR=1 V=1 GITVERSION=%{hash} CROSS_COMPILE="" bin-i386-efi/${rom}.efidrv
  make NO_WERROR=1 V=1 GITVERSION=%{hash} CROSS_COMPILE="" bin-x86_64-efi/${rom}.efidrv
  vid="0x${rom%%????}"
  did="0x${rom#????}"
  EfiRom -f "$vid" -i "$did" --pci23 \
         -b  bin/${rom}.rom \
         -ec bin-i386-efi/${rom}.efidrv \
         -ec bin-x86_64-efi/${rom}.efidrv \
         -o  bin-combined/${rom}.rom
  EfiRom -d  bin-combined/${rom}.rom
done

%endif

%install
%ifarch %{buildarches}
mkdir -p %{buildroot}/%{_datadir}/%{name}/
mkdir -p %{buildroot}/%{_datadir}/%{name}.efi/
pushd src/bin/

cp -a undionly.kpxe ipxe.{iso,usb,dsk,lkrn} %{buildroot}/%{_datadir}/%{name}/

for fmt in %{formats};do
 for img in *.${fmt};do
      if [ -e $img ]; then
   cp -a $img %{buildroot}/%{_datadir}/%{name}/
   echo %{_datadir}/%{name}/$img >> ../../${fmt}.list
  fi
 done
done
popd

# the roms supported by qemu will be packaged separatedly
# remove from the main rom list and add them to qemu.list
for fmt in rom ;do
 for rom in %{qemuroms} ; do
  sed -i -e "/\/${rom}.${fmt}/d" ${fmt}.list
  echo %{_datadir}/%{name}/${rom}.${fmt} >> qemu.${fmt}.list
 done
done
for rom in %{qemuroms}; do
  cp src/bin-combined/${rom}.rom %{buildroot}/%{_datadir}/%{name}.efi/
  echo %{_datadir}/%{name}.efi/${rom}.rom >> qemu.rom.list
done
%endif

%ifarch %{buildarches}
%files bootimgs
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ipxe.iso
%{_datadir}/%{name}/ipxe.usb
%{_datadir}/%{name}/ipxe.dsk
%{_datadir}/%{name}/ipxe.lkrn
%{_datadir}/%{name}/undionly.kpxe
%doc COPYING COPYING.GPLv2 COPYING.UBDL USAGE

%files roms -f rom.list
%dir %{_datadir}/%{name}
%doc COPYING COPYING.GPLv2 COPYING.UBDL

%files roms-qemu -f qemu.rom.list
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}.efi
%doc COPYING COPYING.GPLv2 COPYING.UBDL
%endif

%changelog
* Fri May 06 2016 fj <fujiang.zhu@i-soft.com.cn> - 20150407-4.gitdc795b9f
- rebuilt for xen

