%global apiversion 0.4

Name:		libwps
Version:	0.4.2
Release:	2%{?dist}
Summary:	A library for import of Microsoft Works documents

License:	LGPLv2+ or MPLv2.0
URL:		http://libwps.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	doxygen
BuildRequires:	help2man
BuildRequires:	pkgconfig(librevenge-0.0)

%description
%{name} is a library for import of Microsoft Works text documents,
spreadsheets and (in a limited way) databases.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary:	Tools to transform Microsoft Works documents into other formats
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Microsoft Works documents into other formats.
Currently supported: CSV, HTML, raw, text

%package doc
Summary:	Documentation of %{name} API
BuildArch:	noarch

%description doc
The %{name}-doc package contains documentation files for %{name}

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror --with-sharedptr=c++11
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

export LD_LIBRARY_PATH=`pwd`/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'convert Works spreadsheet into CSV' -o wks2csv.1 ./src/conv/wks2csv/.libs/wks2csv
help2man -N -n 'debug the conversion library' -o wks2raw.1 ./src/conv/wks2raw/.libs/wks2raw
help2man -N -n 'convert Works spreadsheet into plain text' -o wks2text.1 ./src/conv/wks2text/.libs/wks2text
help2man -N -n 'debug the conversion library' -o wps2raw.1 ./src/conv/raw/.libs/wps2raw
help2man -N -n 'convert Works document into HTML' -o wps2html.1 ./src/conv/html/.libs/wps2html
help2man -N -n 'convert Works document into plain text' -o wps2text.1 ./src/conv/text/.libs/wps2text

%install
make install INSTALL="install -p" DESTDIR="%{buildroot}" 
rm -f %{buildroot}%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}%{_defaultdocdir}/%{name}

install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 wks2*.1 wps2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LGPL COPYING.MPL CREDITS NEWS README
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc HACKING
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files tools
%{_bindir}/wks2csv
%{_bindir}/wks2raw
%{_bindir}/wks2text
%{_bindir}/wps2html
%{_bindir}/wps2raw
%{_bindir}/wps2text
%{_mandir}/man1/wks2csv.1*
%{_mandir}/man1/wks2raw.1*
%{_mandir}/man1/wks2text.1*
%{_mandir}/man1/wps2html.1*
%{_mandir}/man1/wps2raw.1*
%{_mandir}/man1/wps2text.1*

%files doc
%doc COPYING.LGPL COPYING.MPL
%doc docs/doxygen/html

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.4.2-2
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
