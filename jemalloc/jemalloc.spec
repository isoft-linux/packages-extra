Name:           jemalloc
Version:        4.0.0

Release:        1%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.canonware.com/jemalloc/
Source0:        http://www.canonware.com/download/jemalloc/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch6:         jemalloc-4.0.0.negative_bitshift.patch

BuildRequires:  /usr/bin/xsltproc
%ifnarch s390
BuildRequires:  valgrind-devel
%endif

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%patch6 -p1

%build
%ifarch i686
CFLAGS="%{optflags} -msse2"
%endif

%configure
make %{?_smp_mflags}

%check
make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README VERSION
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh

%files devel
%defattr(-,root,root,-)
%{_bindir}/jeprof
%{_bindir}/jemalloc-config
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_libdir}/pkgconfig/jemalloc.pc
%{_mandir}/man3/jemalloc.3*
%doc doc/jemalloc.html


%changelog
* Mon Aug 31 2015 Cjacker <cjacker@foxmail.com>
- initial build.
