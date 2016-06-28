Name:           seabios
Version:        1.8.1
Release:        3
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS

Source0:        http://code.coreboot.org/p/seabios/downloads/get/%{name}-%{version}.tar.gz

Source10:       config.vga.cirrus
Source11:       config.vga.isavga
Source12:       config.vga.qxl
Source13:       config.vga.stdvga
Source14:       config.vga.vmware
Source15:       config.csm
Source16:       config.coreboot
Source17:       config.seabios-128k
Source18:       config.seabios-256k

BuildRequires: python iasl
#BuildRequires: binutils-x86_64-linux-gnu gcc-x86_64-linux-gnu

Requires: %{name}-bin = %{version}-%{release}
Requires: seavgabios-bin = %{version}-%{release}
Buildarch: noarch

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

# Similarly, tell RPM to not complain about x86 roms being shipped noarch
%global _binaries_in_noarch_packages_terminate_build   0

# You can build a debugging version of the BIOS by setting this to a
# value > 1.  See src/config.h for possible values, but setting it to
# a number like 99 will enable all possible debugging.  Note that
# debugging goes to a special qemu port that you have to enable.  See
# the SeaBIOS top-level README file for the magic qemu invocation to
# enable this.
%global debug_level 1


%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package bin
Summary: Seabios for x86
Buildarch: noarch


%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package -n seavgabios-bin
Summary: Seavgabios for x86
Buildarch: noarch
Obsoletes: vgabios

%description -n seavgabios-bin
SeaVGABIOS is an open-source VGABIOS implementation.


%prep
%setup -q

# Makefile changes version to include date and buildhost
sed -i 's,VERSION=%{version}.*,VERSION=%{version},g' Makefile


%build
export CFLAGS="$RPM_OPT_FLAGS"
mkdir binaries

build_bios() {
    make clean distclean
    cp $1 .config
    echo "CONFIG_DEBUG_LEVEL=%{debug_level}" >> .config
    make oldnoconfig V=1

    make V=1 \
        HOSTCC=gcc \
        CC=gcc \
        AS=as \
        LD=ld \
        OBJCOPY=objcopy \
        OBJDUMP=objdump \
        STRIP=strip $4

    cp out/$2 binaries/$3
}

# seabios
build_bios %{SOURCE15} Csm16.bin bios-csm.bin
build_bios %{SOURCE16} bios.bin.elf bios-coreboot.bin
build_bios %{SOURCE17} bios.bin bios.bin
build_bios %{SOURCE18} bios.bin bios-256k.bin
cp out/src/fw/*dsdt*.aml binaries

# seavgabios
for config in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14}; do
    name=${config#*config.vga.}
    build_bios ${config} vgabios.bin vgabios-${name}.bin out/vgabios.bin
done


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seabios
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seavgabios
install -m 0644 binaries/bios.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios.bin
install -m 0644 binaries/bios-256k.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-256k.bin
install -m 0644 binaries/bios-csm.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-csm.bin
install -m 0644 binaries/bios-coreboot.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-coreboot.bin
install -m 0644 binaries/*.aml $RPM_BUILD_ROOT%{_datadir}/seabios
install -m 0644 binaries/vgabios*.bin $RPM_BUILD_ROOT%{_datadir}/seavgabios


%files
%doc COPYING COPYING.LESSER README


%files bin
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios*.bin
%{_datadir}/seabios/*.aml

%files -n seavgabios-bin
%dir %{_datadir}/seavgabios/
%{_datadir}/seavgabios/vgabios*.bin


%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 1.8.1-3
- rebuilt for xen

