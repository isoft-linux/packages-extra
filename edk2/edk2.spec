%define SVNDATE   20151127
%define SVNREV    18975

Name:		edk2
Version:	%{SVNDATE}svn%{SVNREV}
Release:	2%{?dist}
Summary:	EFI Development Kit II

# There are no formal releases from upstream.
# Tarballs are created with:

# svn export -r ${SVNREV} \
#     https://svn.code.sf.net/p/edk2/code/trunk/edk2/BaseTools edk2-buildtools-r${SVNREV}
# rm -rf edk2-buildtools-r${SVNREV}/Bin
# tar -cv edk2-buildtools-r${SVNREV} | xz -6 > edk2-buildtools-r${SVNREV}.tar.xz
Source0:	edk2-buildtools-r%{SVNREV}.tar.xz
Patch1:		basetools-arm.patch

License:	BSD
Group:		Applications/Emulators
URL:		http://sourceforge.net/apps/mediawiki/tianocore/index.php?title=EDK2

# We need to build tools everywhere, but how is still an open question
# https://bugzilla.redhat.com/show_bug.cgi?id=992180
ExclusiveArch:	%{ix86} x86_64 %{arm}

BuildRequires:	python2-devel
BuildRequires:	libuuid-devel

Requires:	edk2-tools%{?_isa} = %{version}-%{release}
Requires:	edk2-tools-doc%{?_isa} = %{version}-%{release}

%description
EDK II is a development code base for creating UEFI drivers, applications
and firmware images.

%package tools
Summary:	EFI Development Kit II Tools
Group:		Development/Tools
Requires:	edk2-tools-python = %{version}-%{release}

%description tools
This package provides tools that are needed to
build EFI executables and ROMs using the GNU tools.

%package tools-python
Summary:	EFI Development Kit II Tools
Group:		Development/Tools
Requires:	python
BuildArch:      noarch

%description tools-python
This package provides tools that are needed to build EFI executables
and ROMs using the GNU tools.  You do not need to install this package;
you probably want to install edk2-tools only.

%package tools-doc
Summary:	Documentation for EFI Development Kit II Tools
Group:		Development/Tools

%description tools-doc
This package documents the tools that are needed to
build EFI executables and ROMs using the GNU tools.

%prep
%setup -q -n edk2-buildtools-r%{SVNREV}
%patch1 -p1

%build
export WORKSPACE=`pwd`

# Build is broken if MAKEFLAGS contains -j option.
unset MAKEFLAGS
make

%install
mkdir -p %{buildroot}%{_bindir}
install	\
	Source/C/bin/BootSectImage \
	Source/C/bin/EfiLdrImage \
	Source/C/bin/EfiRom \
	Source/C/bin/GenCrc32 \
	Source/C/bin/GenFfs \
	Source/C/bin/GenFv \
	Source/C/bin/GenFw \
	Source/C/bin/GenPage \
	Source/C/bin/GenSec \
	Source/C/bin/GenVtf \
	Source/C/bin/GnuGenBootSector \
	Source/C/bin/LzmaCompress \
	BinWrappers/PosixLike/LzmaF86Compress \
	Source/C/bin/Split \
	Source/C/bin/TianoCompress \
	Source/C/bin/VfrCompile \
	Source/C/bin/VolInfo \
	%{buildroot}%{_bindir}

ln -f %{buildroot}%{_bindir}/GnuGenBootSector \
	%{buildroot}%{_bindir}/GenBootSector

mkdir -p %{buildroot}%{_datadir}/%{name}
install \
        BuildEnv \
        %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}/Conf
install \
        Conf/build_rule.template \
        Conf/tools_def.template \
        Conf/target.template \
        %{buildroot}%{_datadir}/%{name}/Conf

mkdir -p %{buildroot}%{_datadir}/%{name}/Scripts
install \
        Scripts/GccBase.lds \
        %{buildroot}%{_datadir}/%{name}/Scripts

cp -R Source/Python %{buildroot}%{_datadir}/%{name}/Python

find %{buildroot}%{_datadir}/%{name}/Python -name "*.pyd" | xargs rm

for i in build BPDG Ecc GenDepex GenFds GenPatchPcdTable PatchPcdValue TargetTool Trim UPT; do
  echo '#!/bin/sh
PYTHONPATH=%{_datadir}/%{name}/Python
export PYTHONPATH
exec python '%{_datadir}/%{name}/Python/$i/$i.py' "$@"' > %{buildroot}%{_bindir}/$i
  chmod +x %{buildroot}%{_bindir}/$i
done

%files tools
%{_bindir}/BootSectImage
%{_bindir}/EfiLdrImage
%{_bindir}/EfiRom
%{_bindir}/GenBootSector
%{_bindir}/GenCrc32
%{_bindir}/GenFfs
%{_bindir}/GenFv
%{_bindir}/GenFw
%{_bindir}/GenPage
%{_bindir}/GenSec
%{_bindir}/GenVtf
%{_bindir}/GnuGenBootSector
%{_bindir}/LzmaCompress
%{_bindir}/LzmaF86Compress
%{_bindir}/Split
%{_bindir}/TianoCompress
%{_bindir}/VfrCompile
%{_bindir}/VolInfo
%{_datadir}/%{name}/BuildEnv
%{_datadir}/%{name}/Conf/
%{_datadir}/%{name}/Scripts/

%files tools-python
%{_bindir}/build
%{_bindir}/BPDG
%{_bindir}/Ecc
%{_bindir}/GenDepex
%{_bindir}/GenFds
%{_bindir}/GenPatchPcdTable
%{_bindir}/PatchPcdValue
%{_bindir}/TargetTool
%{_bindir}/Trim
%{_bindir}/UPT
%{_datadir}/%{name}/Python/

%files tools-doc
%doc UserManuals/BootSectImage_Utility_Man_Page.rtf
%doc UserManuals/Build_Utility_Man_Page.rtf
%doc UserManuals/EfiLdrImage_Utility_Man_Page.rtf
%doc UserManuals/EfiRom_Utility_Man_Page.rtf
%doc UserManuals/GenBootSector_Utility_Man_Page.rtf
%doc UserManuals/GenCrc32_Utility_Man_Page.rtf
%doc UserManuals/GenDepex_Utility_Man_Page.rtf
%doc UserManuals/GenFds_Utility_Man_Page.rtf
%doc UserManuals/GenFfs_Utility_Man_Page.rtf
%doc UserManuals/GenFv_Utility_Man_Page.rtf
%doc UserManuals/GenFw_Utility_Man_Page.rtf
%doc UserManuals/GenPage_Utility_Man_Page.rtf
%doc UserManuals/GenPatchPcdTable_Utility_Man_Page.rtf
%doc UserManuals/GenSec_Utility_Man_Page.rtf
%doc UserManuals/GenVtf_Utility_Man_Page.rtf
%doc UserManuals/LzmaCompress_Utility_Man_Page.rtf
%doc UserManuals/PatchPcdValue_Utility_Man_Page.rtf
%doc UserManuals/SplitFile_Utility_Man_Page.rtf
%doc UserManuals/TargetTool_Utility_Man_Page.rtf
%doc UserManuals/TianoCompress_Utility_Man_Page.rtf
%doc UserManuals/Trim_Utility_Man_Page.rtf
%doc UserManuals/VfrCompiler_Utility_Man_Page.rtf
%doc UserManuals/VolInfo_Utility_Man_Page.rtf

%changelog
* Fri May 06 2016 fj <fujiang.zhu@i-soft.com.cn> - 20151127svn18975-2
- rebuilt for xen

