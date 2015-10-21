Name:           kcm-systemd
Version:        1.2.0
Release:        5 
Summary:        Systemd control module for KDE

License:        GPLv3+
URL:            http://kde-apps.org/content/show.php/Kcmsystemd?content=161871
Source0:        http://download.kde.org/stable/systemd-kcm/systemd-kcm-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext
BuildRequires:  boost-devel
# we need the unified libsystemd.so, which was introduced in systemd 209
BuildRequires:  systemd-devel >= 209
BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-rpm-macros

%description
Systemd control module for KDE. It provides a graphical frontend for the systemd
daemon, which allows for viewing and controlling systemd units, as well as
modifying configuration files. In integrates in the System Settings dialogue in
KDE.

%prep
%setup -q -n systemd-kcm-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../
popd
make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

#already in systemsettings.
rm -rf %{buildroot}%{_kf5_datadir}/kservices5/settings-system-administration.desktop

%find_lang systemd-kcm

%files -f systemd-kcm.lang
%doc NEWS README.md
%{_kf5_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmsystemd.conf
%{_kf5_qtplugindir}/kcm_systemd.so
%{_kf5_libexecdir}/kauth/kcmsystemdhelper
%{_kf5_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmsystemd.service
%{_kf5_datadir}/kservices5/kcm_systemd.desktop
%{_kf5_datadir}/polkit-1/actions/org.kde.kcontrol.kcmsystemd.policy

%changelog
* Wed Oct 14 2015 Cjacker <cjacker@foxmail.com>
- move settings-system-administration.desktop to systemsettings package.

* Thu Sep 03 2015 Cjacker <cjacker@foxmail.com>
- rebuilt with new boost
