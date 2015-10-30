Name: radare2
Version: 0.9.9
Release: 3%{?dist}
Summary: %{name} reverse engineering framework
License: GPLv3+ 
URL: http://www.radare.org
Source0: http://rada.re/get/radare2-%{version}.tar.xz 
#capstone git
Source1: capstone.tar.gz

BuildRequires:  file-devel
Requires:	%{name}-devel

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
The %{name} is a reverse-engineering framework that is multi-architecture,
multi-platform, and highly scriptable.  %{name} provides a hexadecimal
editor, wrapped I/O, file system support, debugger support, diffing
between two functions or binaries, and code analysis at opcode,
basic block, and function levels.

%package	devel
Summary:        Development files for the %{name} package
Requires: %{name} = %{version}-%{release}

%description	devel
Development files for the %{name} package. See %{name} package for more
 information.

%prep
%setup -q 
#do not use shipped capstone, use git instead.
rm -rf shlr/capstone
tar zxf %{SOURCE1} -C shlr

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
# Use system libmagic rather than bundled
%configure --with-sysmagic --without-syscapstone

#The make fails if _smp_mflags passed on command line
CFLAGS="%{optflags} -fPIC -I. -Iinclude -I../include" make

# Do not run the testsuite yet
# %check
# make tests

%install
make install DESTDIR="%{buildroot}"
chmod 0755 %{buildroot}/%{_libdir}/%{name}/%{version}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc %{_datadir}/doc/%{name}
%{_bindir}/r*
%{_libdir}/%{name}
%{_libdir}/libr*.so.*
%{_exec_prefix}/lib/%{name}
%{_mandir}/man1/r*.1.*

%files  devel
%{_libdir}/libr*.so
%{_includedir}/libr/
%{_libdir}/pkgconfig/*.pc
%{_datarootdir}/%{name}

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.9.9-3
- Rebuild

* Sat Oct 10 2015 Cjacker <cjacker@foxmail.com>
- Initial package
