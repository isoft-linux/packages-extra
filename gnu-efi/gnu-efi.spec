Summary: Development Libraries and headers for EFI
Name: gnu-efi
Version: 3.0.2
Release: 3%{?dist}
Epoch:	1
License: BSD 
URL: ftp://ftp.hpl.hp.com/pub/linux-ia64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: %{ix86} x86_64 ia64 aarch64
BuildRequires: git
Source: http://superb-dca2.dl.sourceforge.net/project/gnu-efi/gnu-efi-%{version}.tar.bz2
Patch0001: 0001-Add-setjmp-back-once-again.patch

%define debug_package %{nil}

# Figure out the right file path to use
%global efidir %(eval grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/')

%ifarch x86_64
%global efiarch x86_64
%endif
%ifarch aarch64
%global efiarch aarch64
%endif
%ifarch %{ix86}
%global efiarch ia32
%endif

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%package devel
Summary: Development Libraries and headers for EFI
Obsoletes: gnu-efi < 3.0.1-1
Requires: gnu-efi

%description devel
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%package utils
Summary: Utilities for EFI systems

%description utils
This package contains utilties for debugging and developing EFI systems.

%prep
%setup -q -n gnu-efi-%{version}
%patch0001 -p1

%build
# Package cannot build with %{?_smp_mflags}.
make
make apps

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_libdir}

make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install

mkdir -p %{buildroot}/%{_libdir}/gnuefi
mv %{buildroot}/%{_libdir}/*.lds %{buildroot}/%{_libdir}/*.o %{buildroot}/%{_libdir}/gnuefi

mkdir -p %{buildroot}/boot/efi/EFI/%{efidir}/
mv %{efiarch}/apps/{route80h.efi,modelist.efi} %{buildroot}/boot/efi/EFI/%{efidir}/

%clean
rm -rf %{buildroot}

%files
%{_libdir}/*

%files devel
%defattr(-,root,root,-)
%doc README.* ChangeLog
%{_includedir}/efi

%files utils
%dir /boot/efi/EFI/%{efidir}/
%attr(0644,root,root) /boot/efi/EFI/%{efidir}/*.efi

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1:3.0.2-3
- Rebuild

