Name: libabigail
Version: 1.0
Release: 1.git
Summary: Set of ABI analysis tools

License: LGPLv3+
URL: https://sourceware.org/libabigail/
#  git clone git://sourceware.org/git/libabigail.git
Source0: %{name}.tar.xz

BuildRequires: libtool
BuildRequires: libelfutils-devel
BuildRequires: libxml2-devel
BuildRequires: doxygen
BuildRequires: python-sphinx
BuildRequires: texinfo
BuildRequires: dos2unix
BuildRequires: dpkg

%description
The libabigail package comprises five command line utilities: abidiff,
abipkgdiff, abicompat, abidw and abilint.  The abidiff command line
tool compares the ABI of two ELF shared libraries and emits meaningful
textual reports about changes impacting exported functions, variables
and their types.  abipkgdiff compares the ABIs of ELF binaries
contained in two packages.  abicompat checks if a subsequent version
of a shared library is still compatible with an application that is
linked against it.  abidw emits an XML representation of the ABI of a
given ELF shared library. abilint checks that a given XML
representation of the ABI of a shared library is correct.

Install libabigail if you need to compare the ABI of ELF shared
libraries.

%package devel
Summary: Shared library and header files to write ABI analysis tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains a shared library and the associated header files
that are necessary to develop applications that use the C++ Libabigail
library.  The library provides facilities to analyze and compare
application binary interfaces of shared libraries in the ELF format.


%package doc
Summary: Man pages, texinfo files and html manuals of libabigail
Requires(post): info
Requires(preun): info

%description doc
This package contains documentation for the libabigail tools in the
form of man pages, texinfo documentation and API documentation in html
format.

%prep
%setup -n %{name}

%build
autoreconf -ivf
%configure --disable-silent-rules --disable-zip-archive --disable-static 
make %{?_smp_mflags}
pushd doc
make html-doc
pushd manuals
make html-doc
make man
popd
popd

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Install man and texinfo files as they are not installed by the
# default 'install' target of the makefile.
make -C doc/manuals install-man-and-info-doc DESTDIR=%{buildroot}
dos2unix doc/manuals/html/_static/jquery.js

rm -rf %{buildroot}%{_indofir}
%check
make check || (cat tests/test-suite.log && exit 2)

if test $? -ne 0; then
  cat tests/tests-suite.log
fi

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/abicompat
%{_bindir}/abidiff
%{_bindir}/abidw
%{_bindir}/abilint
%{_bindir}/abipkgdiff
%{_libdir}/libabigail.so.0
%{_libdir}/libabigail.so.0.0.0
%doc AUTHORS ChangeLog
%license COPYING COPYING-LGPLV3 COPYING-GPLV3

%files devel
%{_libdir}/libabigail.so
%{_libdir}/pkgconfig/libabigail.pc
%{_includedir}/*
%{_datadir}/aclocal/abigail.m4

%files doc
%license COPYING  COPYING-LGPLV3 COPYING-GPLV3
%doc doc/manuals/html/*
%{_mandir}/man1/*
%{_mandir}/man7/*

%changelog
