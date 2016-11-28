Name:    kf5-libkcddb
Summary: CDDB retrieval library 
Version: 16.11.80
Release: 2%{?dist}

License: GPLv2+
URL:     https://github.com/isoft-linux/libkcddb
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
#Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

#git clone git://anongit.kde.org/libkcddb
#git checkout kf5
Source0: libkcddb-%{version}.tar.bz2
Patch0: libkcddb-16.11.80-cmake_for_low_version_build.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-kdoctools-devel

BuildRequires: libmusicbrainz-devel

%description
%{summary}

%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.


%prep
%autosetup -n libkcddb-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_kf5_qtplugindir}/kcm_cddb.so
%{_kf5_libdir}/libKF5CddbWidgets.so.16*
%{_kf5_libdir}/libKF5Cddb.so.16*
%{_kf5_docdir}/HTML/*/kcontrol/cddbretrieval5/
%{_kf5_datadir}/kservices5/libkcddb.desktop
%{_kf5_datadir}/config.kcfg/libkcddb5.kcfg


%files devel
%{_kf5_includedir}/kcddb_version.h
%{_kf5_includedir}/KCddb
%{_kf5_libdir}/libKF5CddbWidgets.so
%{_kf5_libdir}/libKF5Cddb.so
%{_kf5_libdir}/cmake/KF5Cddb/
%{_kf5_archdatadir}/mkspecs/modules/qt_KCddb.pri


%changelog
* Mon Nov 28 2016 sulit <sulitsrc@gmail.com> - 16.11.80-2
- rebuild it for v4

* Mon Nov 28 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 16.11.80-1
- 16.11.80-1

* Thu Jul 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 16.07.0-2
- 16.07.0
- SOVERSION 16

* Tue Jul 19 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.24.0-3
- 5.24.0
- Rearch.
- Use KF5 style header include.

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 5.0.0-4.git
- Rebuild

