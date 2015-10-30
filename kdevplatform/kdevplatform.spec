%define kdevelop_ver 4.90.90

Name:           kdevplatform
Summary:        Libraries for use by KDE development tools
Version:        4.90.90 
Release:        2%{?dist}

License:        GPLv2
URL:            https://projects.kde.org/projects/extragear/kdevelop/kdevplatform
Source0:        http://download.kde.org/stable/kdevelop/%{kdevelop_ver}/src/kdevplatform-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: pcre-devel
BuildRequires: subversion-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kitemmodels-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-sonnet-devel
BuildRequires: kf5-ktexteditor-devel
BuildRequires: kf5-threadweaver-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-kxmlgui-devel

BuildRequires: grantlee-qt5-devel
BuildRequires: libkomparediff2-devel

%description
KDE Development platform, the foundations upon which
KDevelop and Quanta are built.

%package devel
Summary:  Developer files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: boost-devel
Requires: subversion-devel

%description devel
%{summary}.


%prep
%setup -q -n kdevplatform-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%{_sysconfdir}/xdg/*
%{_kf5_bindir}/kdev_dbus_socket_transformer
%{_kf5_bindir}/kdev_format_source
%{_kf5_bindir}/kdevplatform_shell_environment.sh
%{_kf5_datadir}/kservicetypes5/kdevelopplugin.desktop
%{_kf5_datadir}/kdevcodegen
%{_kf5_datadir}/kxmlgui5/*
%{_kf5_datadir}/kdevcodeutils

%{_kf5_libdir}/lib*.so.*
%{_libdir}/qt5/qml/org/kde/kdevplatform
%{_kf5_qtplugindir}/kdevplatform
%{_kf5_qtplugindir}/grantlee

%{_kf5_datadir}/icons/hicolor/*/*/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%{_kf5_libdir}/lib*.so
%{_includedir}/kdevplatform
%{_kf5_libdir}/cmake/KDevPlatform


%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 4.90.90-2
- Initial build
