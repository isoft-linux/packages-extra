Name:    kf5-libkcddb
Summary: CDDB retrieval library 
Version: 5.0.0
Release: 3.git%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdegraphics/libs/libkexiv2
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
#Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

#git clone git://anongit.kde.org/libkcddb
#git checkout kf5
Source0: libkcddb.tar.gz

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

BuildRequires: libmusicbrainz-devel

%description
%{summary}

%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.


%prep
%autosetup -n libkcddb

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
%{_kf5_libdir}/libkcddbwidgets.so.5*
%{_kf5_libdir}/libkcddb.so.5*
%{_kf5_docdir}/HTML/*/kcontrol/cddbretrieval/
%{_kf5_datadir}/kservices5/libkcddb.desktop
%{_kf5_datadir}/config.kcfg/libkcddb.kcfg


%files devel
%{_kf5_libdir}/libkcddbwidgets.so
%{_kf5_libdir}/libkcddb.so
%{_includedir}/libkcddb/
%{_libdir}/cmake/libkcddb/


%changelog
