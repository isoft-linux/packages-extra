%global _python_bytecompile_errors_terminate_build 0

%define kdevelop_ver 4.90.90

Name:           kdev-python
Summary:        Python development plugin for Kdevelop
Version:        4.90.90 
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
%{_kf5_qtplugindir}/kdevplatform/24/kdevpdb.so
%{_kf5_qtplugindir}/kdevplatform/24/kdevpythonlanguagesupport.so

%{_kf5_datadir}/kdevappwizard/templates/*
%dir %{_kf5_datadir}/kdevpythonsupport
%{_kf5_datadir}/kdevpythonsupport/*

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 4.90.90-3
- Initial build

