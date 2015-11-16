Name: kcm-wacomtablet
Version: 2.1.0
Release: 2.git 
Summary: KDE Config Module for Wacom Tablets

License: GPLv2+ 
URL: https://projects.kde.org/projects/extragear/base/wacomtablet

#git clone -b kf5-port git://anongit.kde.org/wacomtablet
Source0: wacomtablet.tar.gz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  libxcb-devel
BuildRequires:  libX11-devel

Requires: xorg-x11-drv-wacom

%description
%{summary}

%prep
%setup -q -n wacomtablet

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd
make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%{_kf5_bindir}/kde_wacom_tabletfinder
%{_kf5_qtplugindir}/kded_wacomtablet.so
%{_kf5_qtplugindir}/plasma/dataengine/plasma_engine_wacomtablet.so
%{_kf5_qtplugindir}/kcm_wacomtablet.so
%{_kf5_datadir}/knotifications5/wacomtablet.notifyrc
%{_kf5_datadir}/wacomtablet
%{_datadir}/applications/kde_wacom_tabletfinder.desktop
%{_kf5_datadir}/dbus-1/interfaces/org.kde.Wacom.xml
%{_kf5_datadir}/kservices5/kcm_wacomtablet.desktop
%{_kf5_datadir}/kservices5/kded/wacomtablet.desktop
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.wacomtablet.desktop
%{_kf5_datadir}/kservices5/plasma-dataengine-wacomtablet.desktop
%{_docdir}/HTML/en/kcontrol/wacomtablet
%{_kf5_datadir}/plasma/plasmoids/org.kde.wacomtablet
%{_kf5_datadir}/plasma/services/wacomtablet.operations

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 2.1.0-2.git
- Initial build

