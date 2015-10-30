%global apiversion 0.1

Name: libetonyek
Version: 0.1.3
Release: 6%{?dist}
Summary: A library for import of Apple iWork documents

License: MPLv2.0
URL: http://wiki.documentfoundation.org/DLP/Libraries/libetonyek
Source: http://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: glm-devel
BuildRequires: gperf
BuildRequires: help2man
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(mdds)
BuildRequires: pkgconfig(zlib)

%description
%{name} is library for import of documents from Apple iWork applications
(Keynote, Pages and Numbers). It can only import the older format
(Keynote 2-5, Pages 1-4, Numbers 1-2). The support for Numbers is only
minimal at the moment.

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
Summary: Tools to transform Apple iWork documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Apple iWork documents into other formats. Currently
supported: CSV, HTML, SVG, text, and raw.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

export LD_LIBRARY_PATH=`pwd`/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'debug the conversion library' -o key2raw.1 ./src/conv/raw/.libs/key2raw
help2man -N -n 'debug the conversion library' -o numbers2raw.1 ./src/conv/raw/.libs/numbers2raw
help2man -N -n 'debug the conversion library' -o pages2raw.1 ./src/conv/raw/.libs/pages2raw
help2man -N -n 'convert Numbers spreadsheet into CSV' -o numbers2csv.1 ./src/conv/csv/.libs/numbers2csv
help2man -N -n 'convert Pages document into HTML' -o pages2html.1 ./src/conv/html/.libs/pages2html
help2man -N -n 'convert Keynote presentation into SVG' -o key2xhtml.1 ./src/conv/svg/.libs/key2xhtml
help2man -N -n 'convert Keynote presentation into plain text' -o key2text.1 ./src/conv/text/.libs/key2text
help2man -N -n 'convert Numbers spreadsheet into plain text' -o numbers2text.1 ./src/conv/text/.libs/numbers2text
help2man -N -n 'convert Pages document into plain text' -o pages2text.1 ./src/conv/text/.libs/pages2text

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 key2*.1 numbers2*.1 pages2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS COPYING FEATURES NEWS README
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%doc COPYING
%doc docs/doxygen/html

%files tools
%{_bindir}/key2raw
%{_bindir}/key2text
%{_bindir}/key2xhtml
%{_bindir}/numbers2csv
%{_bindir}/numbers2raw
%{_bindir}/numbers2text
%{_bindir}/pages2html
%{_bindir}/pages2raw
%{_bindir}/pages2text
%{_mandir}/man1/key2raw.1*
%{_mandir}/man1/key2text.1*
%{_mandir}/man1/key2xhtml.1*
%{_mandir}/man1/numbers2csv.1*
%{_mandir}/man1/numbers2raw.1*
%{_mandir}/man1/numbers2text.1*
%{_mandir}/man1/pages2html.1*
%{_mandir}/man1/pages2raw.1*
%{_mandir}/man1/pages2text.1*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.1.3-6
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.1.3-5
- Initial build. 

