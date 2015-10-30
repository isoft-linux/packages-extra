Name:          qwtpolar
Version:       1.1.1
Release:       5%{?dist}
Summary:       Qwt/Qt Polar Plot Library
License:       LGPLv2 with exceptions
URL:           http://qwtpolar.sourceforge.net
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

# use system qt_install paths
Patch0:        qwtpolar-1.1.1-qt_install_paths.patch
# add pkgconfig support
Patch1:        qwtpolar-1.1.1-pkgconfig.patch
BuildRequires: qwt-devel

%description
The QwtPolar library contains classes for displaying values on a polar
coordinate system. It is an add-on package for the Qwt Library.

%package devel
Summary:        Development Libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the files necessary
to develop applications using QwtPolar.

%package doc
Summary:        Developer documentation for %{name}
BuildArch:      noarch

%description doc
This package contains developer documentation for QwtPolar.


%prep
%setup -q
%patch0 -p1 -b .qt_install_paths
%patch1 -p1 -b .pkgconfig

rm -rf doc/man
chmod 644 COPYING


%build
%{?_qt4_qmake}
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

mv %{buildroot}/%{_qt4_docdir}/html/html \
   %{buildroot}/%{_qt4_docdir}/html/%{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%doc COPYING CHANGES
%{_libdir}/libqwtpolar.so.1*
%{?_qt4_plugindir}/designer/libqwt_polar_designer_plugin.so

%files devel
%{_includedir}/qwt_polar*.h
%{_libdir}/libqwtpolar.so
%{_libdir}/pkgconfig/qwtpolar.pc
%{_qt4_libdir}/qt4/share/mkspecs/features/%{name}*

%files doc
%doc examples
# Own these to avoid needless dep on qt/qt-doc
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%{_qt4_docdir}/html/%{name}/


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.1.1-5
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
