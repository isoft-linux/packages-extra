%define kdevelop_ver 5.0.2 

Name:           kdev-php
Summary:        PHP development plugin for Kdevelop
Version:        5.0.2 
Release:        2%{?dist}

License:        GPLv2
URL:            https://projects.kde.org/projects/extragear/kdevelop/kdevplatform
Source0:        http://download.kde.org/stable/kdevelop/%{kdevelop_ver}/src/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: pcre-devel
BuildRequires: subversion-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils

BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: python
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kdelibs4support-devel
BuildRequires: kf5-threadweaver-devel
BuildRequires: kf5-ktexteditor-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kdevplatform-devel
BuildRequires: kdevelop-pg-qt-devel

Requires: kdevelop

%description
PHP development plugin for Kdevelop

%prep
%setup -q -n %{name}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/lib*.so
%{_kf5_qtplugindir}/kdevplatform/*/*
%{_kf5_datadir}/kdevappwizard/templates/simple_phpapp.tar.bz2
%{_kf5_datadir}/kdevphpsupport/phpunitdeclarations.php
%{_kf5_datadir}/kdevphpsupport/phpfunctions.php
%{_kf5_datadir}/kservices5/kdevphpunitprovider.desktop
%{_kf5_datadir}/kservices5/kcm_kdevphpdocs.desktop
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Fri Nov 25 2016 cjacker - 5.0.2-2
- Update to 5.0.2

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 4.90.90-3
- Initial build

