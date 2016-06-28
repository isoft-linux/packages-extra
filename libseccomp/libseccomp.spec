Summary: Enhanced seccomp library
Name: libseccomp
Version: 2.3.1
Release: 1
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64 mipsel mips64el ppc64 ppc64le s390 s390x
License: LGPLv2
Group: System Environment/Libraries
Source: https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/seccomp/libseccomp
%ifnarch s390
BuildRequires: valgrind
%endif

%description
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%package devel
Summary: Development files used to build applications with libseccomp support
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release} pkgconfig

%description devel
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%package static
Summary: Enhanced seccomp static library
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release} pkgconfig

%description static
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%prep
%setup -q

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}/%{_libdir}"
mkdir -p "%{buildroot}/%{_includedir}"
mkdir -p "%{buildroot}/%{_mandir}"
make V=1 DESTDIR="%{buildroot}" install
rm -f "%{buildroot}/%{_libdir}/libseccomp.la"

%check
make V=1 check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CREDITS
%doc README
%doc CHANGELOG
%doc SUBMITTING_PATCHES
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_libdir}/libseccomp.so
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%files static
%{_libdir}/libseccomp.a

%changelog
* Tue Jun 28 2016 fj <fujiang.zhu@i-soft.com.cn> - 2.3.1-1
- rebuilt for flatpak
