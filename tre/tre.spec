%global commit c2f5d130c91b1696385a6ae0b5bcfd5214bcc9ca
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: tre
Version: 0.8.0
Release: 15.20140228git%{shortcommit}%{?dist}
License: BSD
Source0: https://github.com/laurikari/tre/archive/%{commit}/tre-%{commit}.tar.gz
Patch0: %{name}-chicken.patch
# make internal tests of agrep work with just-built shared library
Patch1: %{name}-tests.patch
# don't force build-time LDFLAGS into tre.pc
Patch2: %{name}-ldflags.patch
Summary: POSIX compatible regexp library with approximate matching
URL: http://laurikari.net/tre/
# rebuild autotools for bug #926655
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: python2-devel

%description
TRE is a lightweight, robust, and efficient POSIX compatible regexp
matching library with some exciting features such as approximate
matching.

%package devel
Requires: tre = %{version}-%{release}
Summary: Development files for use with the tre package

%description devel
This package contains header files and static libraries for use when
building applications which use the TRE library.

%package -n python-%{name}
Summary: Python bindings for the tre library

%description -n python-%{name}
This package contains the python bindings for the TRE library.

%package -n agrep
Summary: Approximate grep utility

%description -n agrep
The agrep tool is similar to the commonly used grep utility, but agrep
can be used to search for approximate matches.

The agrep tool searches text input for lines (or records separated by
strings matching arbitrary regexps) that contain an approximate, or
fuzzy, match to a specified regexp, and prints the matching lines.
Limits can be set on how many errors of each kind are allowed, or
only the best matching lines can be output.

Unlike other agrep implementations, TRE agrep allows full POSIX
regexps of any length, any number of errors, and non-uniform costs.

%prep
%setup -q -n tre-%{commit}
# hack to fix python bindings build
ln -s lib tre
%patch0 -p1 -b .chicken
%patch1 -p1 -b .tests
%patch2 -p1 -b .ldflags
# rebuild autotools for bug #926655
touch ChangeLog
autoreconf -vif

%build
%configure --disable-static --disable-rpath
%{__make} %{?_smp_mflags}
pushd python
%{__python2} setup.py build
popd

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT
pushd python
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
rm $RPM_BUILD_ROOT%{_libdir}/*.la
%find_lang %{name}

%check
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS ChangeLog LICENSE NEWS README THANKS TODO
%doc doc/*.html doc/*.css
%{_libdir}/libtre.so.*

%files devel
%{_libdir}/libtre.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files -n python-%{name}
%attr(0755,root,root) %{python2_sitearch}/tre.so
%{python2_sitearch}/*.egg-info

%files -n agrep
%{_bindir}/agrep
%{_mandir}/man1/agrep.1*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.8.0-15.20140228gitc2f5d13
- Rebuild

