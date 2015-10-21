%global apiversion 0.10

Name: libwpd
Summary: A library for import of WordPerfect documents
Version: 0.10.0
Release: 5%{?dist}
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
URL: http://libwpd.sf.net/
License: LGPLv2+ or MPLv2.0

BuildRequires: doxygen
BuildRequires: help2man
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(zlib)

%description
%{name} is a library for import of WordPerfect documents.

%package tools
Summary: Tools to transform WordPerfect documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform WordPerfect documents into other formats.
Currently supported: HTML, raw, text.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Files for developing with libwpd

%description devel
Includes and definitions for developing with libwpd.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains API documentation for %{name}.

%prep
%setup -q

chmod -x docs/%{name}.dia

%build
%configure --disable-static --disable-werror --disable-silent-rules
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

export LD_LIBRARY_PATH=`pwd`/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'debug the conversion library' -o wpd2raw.1 ./src/conv/raw/.libs/wpd2raw
help2man -N -n 'convert WordPerfect document into HTML' -o wpd2html.1 ./src/conv/html/.libs/wpd2html
help2man -N -n 'convert WordPerfect document into plain text' -o wpd2text.1 ./src/conv/text/.libs/wpd2text

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
# we install API docs directly from build
rm -rf $RPM_BUILD_ROOT/%{_docdir}/%{name}

install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 wpd2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING.LGPL COPYING.MPL CREDITS README
%{_libdir}/%{name}-%{apiversion}.so.*

%files tools
%{_bindir}/wpd2html
%{_bindir}/wpd2raw
%{_bindir}/wpd2text
%{_mandir}/man1/wpd2html.1*
%{_mandir}/man1/wpd2raw.1*
%{_mandir}/man1/wpd2text.1*

%files devel
%doc HACKING TODO
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%{_includedir}/%{name}-%{apiversion}

%files doc
%doc COPYING.LGPL COPYING.MPL
%doc docs/doxygen/html
%doc docs/%{name}.dia
%doc docs/%{name}.png

%changelog
* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
