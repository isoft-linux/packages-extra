Name:    kf5-libkcddb
Summary: CDDB retrieval library 
Version: 5.24.0
Release: 1%{?dist}

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
Source0: libkcddb-5.24.0.tar.bz2

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kcompletion-devel >= %{version}
BuildRequires: kf5-kconfig-devel >= %{version}
BuildRequires: kf5-kconfigwidgets-devel >= %{version}
BuildRequires: kf5-kcoreaddons-devel >= %{version}
BuildRequires: kf5-kdbusaddons-devel >= %{version}
BuildRequires: kf5-kdeclarative-devel >= %{version}
BuildRequires: kf5-kguiaddons-devel >= %{version}
BuildRequires: kf5-ki18n-devel >= %{version}
BuildRequires: kf5-kiconthemes-devel >= %{version}
BuildRequires: kf5-kitemviews-devel >= %{version}
BuildRequires: kf5-kio-devel >= %{version}
BuildRequires: kf5-kjobwidgets-devel >= %{version}
BuildRequires: kf5-knewstuff-devel >= %{version}
BuildRequires: kf5-knotifyconfig-devel >= %{version}
BuildRequires: kf5-knewstuff-devel >= %{version}
BuildRequires: kf5-kservice-devel >= %{version}
BuildRequires: kf5-kwindowsystem-devel >= %{version}
BuildRequires: kf5-kwidgetsaddons-devel >= %{version}
BuildRequires: kf5-kxmlgui-devel >= %{version}
BuildRequires: kf5-kdoctools-devel >= %{version}

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
%{_kf5_libdir}/libKF5CddbWidgets.so.5*
%{_kf5_libdir}/libKF5Cddb.so.5*
%{_kf5_docdir}/HTML/*/kcontrol/cddbretrieval/
%{_kf5_datadir}/kservices5/libkcddb.desktop
%{_kf5_datadir}/config.kcfg/libkcddb.kcfg


%files devel
%{_kf5_includedir}/kcddb_version.h
%{_kf5_includedir}/KCddb
%{_kf5_libdir}/libKF5CddbWidgets.so
%{_kf5_libdir}/libKF5Cddb.so
%{_kf5_libdir}/cmake/KF5Cddb/
%{_kf5_archdatadir}/mkspecs/modules/qt_KCddb.pri


%changelog
* Tue Jul 19 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.24.0-1
- 5.24.0

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 5.0.0-4.git
- Rebuild

