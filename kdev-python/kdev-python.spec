%global _python_bytecompile_errors_terminate_build 0

%define kdevelop_ver 5.0.2 

Name:           kdev-python
Summary:        Python development plugin for Kdevelop
Version:        5.0.2
Release:        3%{?dist}

License:        GPLv2
URL:            https://projects.kde.org/projects/extragear/kdevelop/kdevplatform
Source0:        http://download.kde.org/stable/kdevelop/%{kdevelop_ver}/src/%{name}-%{version}.tar.xz
Patch0:         kdev-python-requires-kdelibs4support-for-missing-kdeversion.h.patch

BuildRequires: boost-devel
BuildRequires: pcre-devel
BuildRequires: subversion-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils

BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: python3 >= 3.5.0
BuildRequires: python3-devel
BuildRequires: kf5-rpm-macros
BuildRequires: qt5-qtbase-devel

BuildRequires: kf5-kdelibs4support-devel
BuildRequires: kf5-threadweaver-devel
BuildRequires: kf5-ktexteditor-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-kitemmodels-devel
BuildRequires: kdevplatform-devel
BuildRequires: kdevelop-pg-qt-devel
BuildRequires: kdevelop-devel
BuildRequires: qt5-qtwebkit-devel
BuildRequires: kf5-attica-devel
BuildRequires: kf5-kauth-devel
BuildRequires: kf5-kbookmarks-devel
BuildRequires: kf5-kcodecs-devel
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-kpackage-devel
BuildRequires: kf5-solid-devel
BuildRequires: kf5-sonnet-devel
BuildRequires: kf5-ktextwidgets-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kitemmodels-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-ktexteditor-devel
BuildRequires: kf5-threadweaver-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-krunner-devel
BuildRequires: kf5-plasma-devel
BuildRequires: kf5-kcrash-devel
BuildRequires: libksysguard-devel
BuildRequires: kf5-karchive-devel
BuildRequires: grantlee-qt5-devel
BuildRequires: kdevelop-pg-qt-devel

Requires: kdevelop

%description
Python development plugin for Kdevelop

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

#smp build failed?
make -C %{_target_platform}
#make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang kdevpython
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f kdevpython.lang
%{_kf5_libdir}/libkdevpythoncompletion.so
%{_kf5_libdir}/libkdevpythonduchain.so
%{_kf5_libdir}/libkdevpythonparser.so
%{_kf5_qtplugindir}/kdevplatform/*/*

%{_kf5_datadir}/kdevappwizard/templates/*
%dir %{_kf5_datadir}/kdevpythonsupport
%{_kf5_datadir}/kdevpythonsupport/*

%changelog
* Mon Nov 28 2016 cjacker - 5.0.2-3
- Update release, build for v5

* Fri Nov 25 2016 cjacker - 5.0.2-2
- Update to 5.0.2

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 4.90.90-3
- Initial build

