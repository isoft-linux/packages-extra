Summary: SELinux binary policy manipulation library 
Name: libsepol
Version: 2.4
Release: 5
License: LGPLv2+
Group: System Environment/Libraries
Source: https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20150202/libsepol-%{version}.tar.gz
URL: https://github.com/SELinuxProject/selinux/wiki
BuildRequires: flex

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package devel
Summary: Header files and libraries used to build policy manipulation tools
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package static
Summary: static libraries used to build policy manipulation tools
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libsepol-static package contains the static libraries and header files
needed for developing applications that manipulate binary policies. 

%prep
%setup -q

# sparc64 is an -fPIC arch, so we need to fix it here
%ifarch sparc64
sed -i 's/fpic/fPIC/g' src/Makefile
%endif

%build
make clean
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_lib} 
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir} 
mkdir -p ${RPM_BUILD_ROOT}%{_includedir} 
mkdir -p ${RPM_BUILD_ROOT}%{_bindir} 
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
make DESTDIR="${RPM_BUILD_ROOT}" LIBDIR="${RPM_BUILD_ROOT}%{_libdir}" SHLIBDIR="${RPM_BUILD_ROOT}/%{_libdir}" install
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolbools
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolusers
rm -f ${RPM_BUILD_ROOT}%{_bindir}/chkcon
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%postun -p /sbin/ldconfig

%files static
%defattr(-,root,root)
%{_libdir}/libsepol.a

%files devel
%defattr(-,root,root)
%{_libdir}/libsepol.so
%{_libdir}/pkgconfig/libsepol.pc
%{_includedir}/sepol/*.h
%{_mandir}/man3/*.3.gz
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%dir %{_includedir}/sepol/cil
%{_includedir}/sepol/cil/*.h

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libsepol.so.1

%changelog
* Wed May 04 2016 fj <fujiang.zhu@i-soft.com.cn> - 2.4-5
- rebuilt for libvirt

