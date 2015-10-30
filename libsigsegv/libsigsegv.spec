Summary: Library for handling page faults in user mode
Name:    libsigsegv
Version: 2.10
Release: 10%{?dist}

License: GPLv2+
URL:     http://libsigsegv.sourceforge.net/
Source0: http://ftp.gnu.org/gnu/libsigsegv/libsigsegv-%{version}.tar.gz

BuildRequires: automake libtool

%description
This is a library for handling page faults in user mode. A page fault
occurs when a program tries to access to a region of memory that is
currently not available. Catching and handling a page fault is a useful
technique for implementing:
  - pageable virtual memory
  - memory-mapped access to persistent databases
  - generational garbage collectors
  - stack overflow handlers
  - distributed shared memory

%package devel
Summary: Development libraries and header files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static libraries for %{name}
Requires: %{name}-devel = %{version}-%{release}
%description static
%{summary}.


%prep
%setup -q

%build
%configure \
  --enable-shared \
  --enable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot} 

make install DESTDIR=%{buildroot}

## unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la


%check
make check


%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libsigsegv.so.2*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libsigsegv.so
%{_includedir}/sigsegv.h

%files static
%defattr(-,root,root,-)
%{_libdir}/libsigsegv.a


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.10-10
- Rebuild

