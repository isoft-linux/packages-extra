%define libselinuxver 2.1.13-1
%define libsepolver 2.1.9-1
Summary: SELinux policy compiler
Name: checkpolicy
Version: 2.3
Release: 6
License: GPLv2
Group: Development/System
Source: http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
#Patch: checkpolicy-rhat.patch
Patch: checkpolicy-sepol.patch

BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: byacc bison flex flex-devel libsepol-static >= %{libsepolver} libselinux-devel  >= %{libselinuxver} 
#BuildRequires: byacc bison flex flex-static libsepol-static >= %{libsepolver} libselinux-devel  >= %{libselinuxver} 

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

This package contains checkpolicy, the SELinux policy compiler.  
Only required for building policies. 

%prep
%setup -q
%patch -p1 -b .sepol

%build
make clean
make LIBDIR="%{_libdir}" CFLAGS="%{optflags}" 
cd test
make LIBDIR="%{_libdir}" CFLAGS="%{optflags}" 

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
make LIBDIR="%{_libdir}" DESTDIR="${RPM_BUILD_ROOT}" install
install test/dismod ${RPM_BUILD_ROOT}%{_bindir}/sedismod
install test/dispol ${RPM_BUILD_ROOT}%{_bindir}/sedispol

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/checkpolicy
%{_bindir}/checkmodule
%{_mandir}/man8/checkpolicy.8.gz
%{_mandir}/man8/checkmodule.8.gz
%{_bindir}/sedismod
%{_bindir}/sedispol

%changelog
* Fri May 06 2016 fj <fujiang.zhu@i-soft.com.cn> - 2.3-6
- rebuilt for xen,add sepol.patch(checkpolicy's version is lower than sepol)

