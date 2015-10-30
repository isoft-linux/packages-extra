Summary: Conversion between character sets and surfaces
Name: recode
Version: 3.6
Release: 42%{?dist}
License: GPLv2+
Url:    http://recode.progiciels-bpi.ca/
Source: http://recode.progiciels-bpi.ca/archives/recode-%{version}.tar.gz
Patch0: recode.patch
Patch1: recode-3.6-getcwd.patch
Patch2: recode-bool-bitfield.patch
Patch3: recode-flex-m4.patch
Patch4: recode-automake.patch
Patch5: recode-format-security.patch

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: libtool
BuildRequires: texinfo


%description
The `recode' converts files between character sets and usages.
It recognizes or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations.  Most RFC 1345 character sets
are supported.

%package devel
Summary: Header files for development using recode
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The `recode' library converts files between character sets and usages.
The library recognizes or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations. Most RFC 1345 character sets
are supported.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .getcwd
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
rm m4/libtool.m4
rm acinclude.m4

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%check
make check

%install
%makeinstall
%find_lang %{name}

# remove unpackaged file from the buildroot
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# remove libtool archives
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING* ChangeLog NEWS README THANKS TODO
%{_mandir}/*/*
%{_infodir}/recode.info*
%{_bindir}/*
%{_libdir}/*.so.0*

%files devel
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 3.6-42
- Initial build

