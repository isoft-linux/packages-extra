%define qt5 1

Name:    qwt
Summary: Qt Widgets for Technical Applications
Version: 6.1.2
Release: 5%{?dist}

License: LGPLv2 with exceptions
URL:     http://qwt.sourceforge.net
Source:  http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

## upstream patches

## upstreamable patches
# fix pkgconfig support
Patch50: qwt-6.1.1-pkgconfig.patch
# use QT_INSTALL_ paths instead of custom prefix
Patch51: qwt-6.1.2-qt_install_paths.patch
# parallel-installable qt5 version
Patch52: qwt-qt5.patch

%if 0%{?qt5}
BuildRequires: pkgconfig(Qt5Concurrent) pkgconfig(Qt5PrintSupport) pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5OpenGL) pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5Designer)
%endif
BuildRequires: pkgconfig(QtGui) pkgconfig(QtSvg)
BuildRequires: pkgconfig(QtDesigner)
# silly buildsys quirk
BuildConflicts: qwt-devel
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}


Provides: qwt6 = %{version}-%{release}
Provides: qwt6%{_isa} = %{version}-%{release}

%description
The Qwt library contains GUI Components and utility classes which are primarily
useful for programs with a technical background.
Besides a 2D plot widget it provides scales, sliders, dials, compasses,
thermometers, wheels and knobs to control or display values, arrays
or ranges of type double.

%package devel
Summary:  Development files for %{name}
Provides: qwt6-devel = %{version}-%{release}
Provides: qwt6-devel%{_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Developer documentation for %{name}
BuildArch: noarch
%description doc
%{summary}.

%if 0%{?qt5}
%package qt5
Summary: Qt5 Widgets for Technical Applications
Provides: qwt6-qt5 = %{version}-%{release}
Provides: qwt6-qt5%{_isa} = %{version}-%{release}
%description qt5
%{summary}.

%package qt5-devel
Summary:  Development files for %{name}-qt5
Provides: qwt6-qt5-devel = %{version}-%{release}
Provides: qwt6-qt5-devel%{_isa} = %{version}-%{release}
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
%description qt5-devel
%{summary}.
%endif


%prep
%setup -q

%patch50 -p1 -b .pkgconfig
%patch51 -p1 -b .qt_install_paths
%patch52 -p1 -b .qt5


%build
%if 0%{?qt5}
mkdir %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%{?qmake_qt5}%{?!qmake_qt5:%{_qt5_qmake}} QWT_CONFIG+=QwtPkgConfig ..

make %{?_smp_mflags}
popd
%endif

mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt4} QWT_CONFIG+=QwtPkgConfig ..

make %{?_smp_mflags}
popd


%install
rm -rf %{buildroot}
%if 0%{?qt5}
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}-qt5
%endif
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

# fixup doc path bogosity
mv %{buildroot}%{_qt4_docdir}/html/html \
   %{buildroot}%{_qt4_docdir}/html/qwt

mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{_qt4_docdir}/html/man/man3 \
   %{buildroot}%{_mandir}/

%if 0%{?qt5}
# nuke qt5 docs, use copies from qt4 build instead 
rm -rfv %{buildroot}%{_qt5_docdir}/html/*

cp -alf %{buildroot}%{_qt4_docdir}/html/qwt/ \
        %{buildroot}%{_qt5_docdir}/html/qwt/
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc README
%{_qt4_libdir}/libqwt.so.6*
%{?_qt4_plugindir}/designer/libqwt_designer_plugin.so
# subpkg ? -- rex
%{_qt4_libdir}/libqwtmathml.so.6*

%files devel
%{_qt4_headerdir}/qwt/
%{_qt4_libdir}/libqwt.so
%{_qt4_libdir}/libqwtmathml.so
%{_qt4_libdir}/qt4/share/mkspecs/features/qwt*
%{_qt4_libdir}/pkgconfig/qwt.pc
%{_qt4_libdir}/pkgconfig/qwtmathml.pc

%files doc
# own these to avoid needless dep on qt/qt-doc
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%{_qt4_docdir}/html/qwt/
%if 0%{?qt5}
%dir %{_qt5_docdir}
%dir %{_qt5_docdir}/html/
%{_qt5_docdir}/html/qwt/
%endif
%{_mandir}/man3/*


%if 0%{?qt5}
%post qt5 -p /sbin/ldconfig
%postun qt5 -p /sbin/ldconfig

%files qt5
%doc COPYING
%doc README
%{_qt5_libdir}/libqwt-qt5.so.6*
%{_qt5_plugindir}/designer/libqwt_designer_plugin.so
%{_qt5_libdir}/libqwtmathml-qt5.so.6*

%files qt5-devel
%{_qt5_headerdir}/qwt/
%{_qt5_libdir}/libqwt-qt5.so
%{_qt5_libdir}/libqwtmathml-qt5.so
%{_qt5_libdir}/qt5/mkspecs/features/qwt*
%{_qt5_libdir}/pkgconfig/Qt5Qwt6.pc
%{_qt5_libdir}/pkgconfig/qwtmathml-qt5.pc
%endif


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 6.1.2-5
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
