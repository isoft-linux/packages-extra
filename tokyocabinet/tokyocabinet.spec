Summary:	A modern implementation of a DBM
Name:		tokyocabinet
Version:	1.4.48
Release:	6%{?dist}
License:	LGPLv2+
URL:		http://fallabs.com/tokyocabinet/
Source:		http://fallabs.com/%{name}/%{name}-%{version}.tar.gz
Patch0:		tokyocabinet-fedora.patch
Patch1:		tokyocabinet-manhelp.patch
BuildRequires:	pkgconfig zlib-devel bzip2-devel autoconf

%description
Tokyo Cabinet is a library of routines for managing a database. It is the 
successor of QDBM. Tokyo Cabinet runs very fast. For example, the time required
to store 1 million records is 1.5 seconds for a hash database and 2.2 seconds
for a B+ tree database. Moreover, the database size is very small and can be up
to 8EB. Furthermore, the scalability of Tokyo Cabinet is great.

%package devel
Summary:	Headers for developing programs that will use %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%package devel-doc
Summary:	Documentation files for developing programs that will use %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
BuildArch:	noarch

%description devel-doc
This package contains documentation files for the libraries and header files
needed for developing with %{name}.

%prep
%setup -q
%patch0 -p0 -b .fedora
%patch1 -p1 -b .manhelp

%build
autoconf
%configure --enable-off64 CFLAGS="$CFLAGS"
make %{?_smp_mflags}
										
%install
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_libdir}/lib%{name}.a

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog COPYING README
%{_bindir}/tc*
%{_libdir}/libtokyocabinet.so.*
%{_libexecdir}/tcawmgr.cgi
%{_mandir}/man1/tc*.gz

%files devel
%{_includedir}/tc*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/t*.gz

%files devel-doc
%doc doc/*

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 1.4.48-6
- Initial build

