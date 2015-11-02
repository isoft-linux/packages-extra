%global apiversion 0.1

Name: libvisio
Version: 0.1.3
Release: 7%{?dist}
Summary: A library for import of Microsoft Visio diagrams

License: MPLv2.0
URL: http://wiki.documentfoundation.org/DLP/Libraries/libvisio
Source: http://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gperf
BuildRequires: help2man
BuildRequires: perl
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(libxml-2.0) >= 2.9.2
BuildRequires: pkgconfig(zlib)

Patch0: 0001-fix-test.patch

%description
%{name} is library providing ability to interpret and import
Microsoft Visio diagrams into various applications. You can find it
being used in libreoffice.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform Microsoft Visio diagrams into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Microsoft Visio diagrams into other formats.
Currently supported: XHTML, raw, plain text.

%prep
%autosetup -p1

%build
export CPPFLAGS='-DBOOST_ERROR_CODE_HEADER_ONLY -DBOOST_SYSTEM_NO_DEPRECATED'
%configure --disable-static --disable-silent-rules
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

export LD_LIBRARY_PATH=`pwd`/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'debug the conversion library' -o vsd2raw.1 ./src/conv/raw/.libs/vsd2raw
help2man -N -n 'convert Visio document into SVG' -o vsd2xhtml.1 ./src/conv/svg/.libs/vsd2xhtml
help2man -N -n 'convert Visio document into plain text' -o vsd2text.1 ./src/conv/text/.libs/vsd2text
help2man -N -n 'debug the conversion library' -o vss2raw.1 ./src/conv/raw/.libs/vss2raw
help2man -N -n 'convert Visio stencil into SVG' -o vss2xhtml.1 ./src/conv/svg/.libs/vss2xhtml
help2man -N -n 'convert Visio stencil into plain text' -o vss2text.1 ./src/conv/text/.libs/vss2text

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# rhbz#1001240 we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 vsd2*.1 vss2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# Workaround time formatting problem in the test
export TZ='CET'
make check %{?_smp_mflags}

%files
%doc AUTHORS COPYING.*
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%doc COPYING.*
%doc docs/doxygen/html

%files tools
%{_bindir}/vsd2raw
%{_bindir}/vsd2text
%{_bindir}/vsd2xhtml
%{_bindir}/vss2raw
%{_bindir}/vss2text
%{_bindir}/vss2xhtml
%{_mandir}/man1/vsd2raw.1*
%{_mandir}/man1/vsd2text.1*
%{_mandir}/man1/vsd2xhtml.1*
%{_mandir}/man1/vss2raw.1*
%{_mandir}/man1/vss2text.1*
%{_mandir}/man1/vss2xhtml.1*

%changelog
* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 0.1.3-7
- Rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.1.3-6
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.1.3-5
- Initial build 

