Summary: An unwinding library
Name: libunwind
Version: 1.1
Release: 11%{?dist}
License: BSD
Source: http://download.savannah.gnu.org/releases/libunwind/libunwind-%{version}.tar.gz
#Fedora specific patch
Patch1: libunwind-disable-setjmp.patch
Patch2: libunwind-aarch64.patch
Patch3: libunwind-fix-ppc64_test_altivec.patch
Patch4: libunwind-arm-default-to-exidx.patch
Patch5: libunwind-1.1-fix-CVE-2015-3239.patch
URL: http://savannah.nongnu.org/projects/libunwind
ExclusiveArch: %{arm} aarch64 hppa ia64 mips ppc %{power64} %{ix86} x86_64

BuildRequires: automake libtool autoconf

# host != target would cause REMOTE_ONLY build even if building i386 on x86_64.
%global _host %{_target_platform}

%description
Libunwind provides a C ABI to determine the call-chain of a program.

%package devel
Summary: Development package for libunwind
Requires: libunwind = %{version}-%{release}

%description devel
The libunwind-devel package includes the libraries and header files for
libunwind.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .default-to-exidx
%patch5 -p1 -b .CVE-2015-3239

%build
aclocal
libtoolize --force
autoheader
automake --add-missing
autoconf
%configure --enable-static --enable-shared
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# /usr/include/libunwind-ptrace.h
# [...] aren't really part of the libunwind API.  They are implemented in
# a archive library called libunwind-ptrace.a.
mv -f $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a-save
rm -f $RPM_BUILD_ROOT%{_libdir}/libunwind*.a
mv -f $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a-save $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace*.so*

%check
echo ====================TESTING=========================
make check || true
echo ====================TESTING END=====================

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_libdir}/libunwind*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libunwind*.so
%{_libdir}/libunwind-ptrace.a
%{_libdir}/pkgconfig/libunwind*.pc
%{_mandir}/*/*
# <unwind.h> does not get installed for REMOTE_ONLY targets - check it.
%{_includedir}/unwind.h
%{_includedir}/libunwind*.h

%changelog
* Tue Oct 27 2015 cjacker - 1.1-11
- Initial build

