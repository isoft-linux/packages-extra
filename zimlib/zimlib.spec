Name: zimlib
Version: 1.2
Release: 2%{?dist}
Summary: Library for reading/writing ZIM files

License: GPLv2+
URL: http://openzim.org/wiki/Main_Page
Source0: http://www.openzim.org/download/%{name}-%{version}.tar.gz

BuildRequires: xz-devel

%description
The zimlib is the standard implementation of the ZIM specification. It is a
library which implements the read and write method for ZIM files. Use zimlib in
your own software - like reader applications - to make them ZIM-capable without
the need having to dig too much into the ZIM file format. zimlib is written in
C++. It also includes the binaries zimsearch and zimdump, for directly
searching and viewing ZIM file contents.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}. 


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}

%install
# notified upstream about non-preserving installation of files. He filed a bug. 
%make_install INSTALL="/usr/bin/install -c -p"


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING 
%{_bindir}/zimdump
%{_bindir}/zimsearch
%{_libdir}/*.so.*

%files devel
%{_includedir}/zim/
%{_libdir}/*.so


%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.0-2
- Initial build

