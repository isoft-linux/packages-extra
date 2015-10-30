Name:           plasma-pa
Version:        5.4.2
Release:        8
Summary:        Plasma Volume Controller 

License:        GPLv2+ and (GPLv2 or GPLv3)
URL:            https://projects.kde.org/projects/kde/workspace/plasma-desktop

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

## upstreamable patches

BuildRequires:  pulseaudio-libs-devel 

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-ksysguard-devel
BuildRequires:  kf5-baloo-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kpeople-devel
BuildRequires:  kf5-kded-devel
BuildRequires:  kf5-kinit-devel >= 5.10.0-3
# libkdeinit5_*
%{?kf5_kinit_requires}

Requires:       kf5-kded

# Desktop
Requires:       plasma-workspace
Requires:       kf5-filesystem

%description
%{summary}.

%prep
%autosetup -p1


%build

mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang kcm_pulseaudio
%find_lang plasma_applet_org.kde.plasma.volume
cat kcm_pulseaudio.lang >>plasma-pa.lang
cat plasma_applet_org.kde.plasma.volume.lang >>plasma-pa.lang

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files -f plasma-pa.lang
%{_kf5_libdir}/libQPulseAudioPrivate.so
%{_kf5_qtplugindir}/kcms/kcm_pulseaudio.so
%{_libdir}/qt5/qml/org/kde/plasma/private/volume
%{_kf5_datadir}/kconf_update/disable_kmix.upd
%{_kf5_datadir}/kconf_update/plasmaVolumeDisableKMixAutostart.pl
%{_kf5_datadir}/kpackage/kcms/kcm_pulseaudio
%{_kf5_datadir}/kservices5/kcm_pulseaudio.desktop
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.plasma.volume.desktop
%{_kf5_datadir}/plasma/plasmoids/org.kde.plasma.volume

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 5.4.2-8
- Rebuild

* Wed Oct 07 2015 Cjacker <cjacker@foxmail.com>
- update to 5.4.2

* Wed Sep 09 2015 Cjacker <cjacker@foxmail.com>
- update to 5.4.1

* Wed Aug 26 2015 Cjacker <cjacker@foxmail.com>
- update to 5.4.0

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 5.3.95

